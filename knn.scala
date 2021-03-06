import Utils.toSpatialIntArray
import spatial.dsl._


@spatial object KNN extends SpatialApp {
  def main(args: Array[String]): Unit = {

    type Q4_4 = FixPt[TRUE, _4, _4]

    @struct class DistLabel(
      dist: Q4_4,
      label: Char
    )

    @struct class LabelCount(
      label: Char,
      count: Char
    )

    val k_num = 5
    val test_size = 15
    val train_size = 135
    val v_len = 4
    
    //dummy data
    //val test_set = (0::test_size, 0::v_len){(i,j) => (i*8).to[Q4_4]}
    //val train_set = (0::train_size, 0::v_len){(i,j) => (10 - i).to[Q4_4]}
    //val train_labels_scala = scala.Array(0,0,0,0,0,1,1,1,1,1)
    //val train_labels = toSpatialIntArray(train_labels_scala)

    //print("test")
    //printMatrix(test_set)
    //print("train")
    //printMatrix(train_set)
    //print("labels")
    //printArray(train_labels)

    val test_set = loadCSV2D[Q4_4](sys.env("TEST_DATA_HOME") + "test.csv", ",")
    val test_labels = loadCSV1D[Char](sys.env("TEST_DATA_HOME") + "test_labels.csv", "\n")
    val train_set = loadCSV2D[Q4_4](sys.env("TEST_DATA_HOME") + "train.csv", ",")
    val train_labels = loadCSV1D[Char](sys.env("TEST_DATA_HOME") + "train_labels.csv", "\n")

    val dTrain = DRAM[Q4_4](train_size.to[Int], v_len.to[Int])
    val dTest = DRAM[Q4_4](test_size.to[Int], v_len.to[Int])
    val dLabels = DRAM[Char](train_size.to[Int])

    setMem(dTrain, train_set)
    setMem(dTest, test_set)
    setMem(dLabels, train_labels)

    // temp test vars
    val distanceDRAM = DRAM[DistLabel](train_size.to[Int], test_size.to[Int])
    val sortedDRAM = DRAM[DistLabel](k_num.to[Int], test_size.to[Int])
    val outputDRAM = DRAM[Char](test_size.to[Int])

    Accel {
      val nTrain = train_size.to[Int]
      val nTest = test_size.to[Int]
      val vLen = v_len.to[Int]
      val k = k_num.to[Int]
      val classes = 3.to[Int]

      val base = 0.to[Int]
      val test_par = 4.to[Int]
      val train_par = 2.to[Int]
      val dist_par = 4.to[Int]
      val load_par = 64.to[Int]
      val step = 1.to[Int]

      val test_sram = SRAM[Q4_4](nTest, vLen)
      val train_sram = SRAM[Q4_4](nTrain, vLen)
      val label_sram = SRAM[Char](nTrain)
      val distances = SRAM[DistLabel](nTrain, nTest)

      test_sram load dTest(base :: nTest, base :: vLen par load_par)
      train_sram load dTrain(base :: nTrain, base :: vLen par load_par)
      label_sram load dLabels(base :: nTrain par load_par)
      
      // calculate the distances in parallel
      Foreach(nTest by step par test_par){ test_idx =>
        Foreach(nTrain by step par train_par){ train_idx =>
          val distance = Reg[Q4_4](0)
          //Reduction for manhattan and chebyshev

          Reduce(distance)(vLen by 1 par dist_par){ i =>
            val pos = test_sram(test_idx, i) - train_sram(train_idx, i)
            val neg = train_sram(train_idx, i) - test_sram(test_idx, i)
            val abs = mux(pos > neg, pos, neg) //jank absolute value function
            abs
          //}{_+_} //this is the manhattan distance
          }{(a,b) => mux(a>b, a, b)} //this is the chebyshev distance
          
          //Reduction for euclidian
          
          //Reduce(distance)(vLen by 1 par dist_par){ i =>
          //    val diff = test_sram(test_idx, i) - train_sram(train_idx, i)
          //    diff*diff //no abs or sqrt needed
          //}{_+_}

          distances(train_idx, test_idx) = DistLabel(distance, label_sram(train_idx))
        }
      }

      // distance output for debugging
      distanceDRAM(base :: nTrain, base :: nTest) store distances

      val sorted_sram = SRAM[DistLabel](k, nTest)

      val sort_par = 32.to[Int]
      val max_dist = 7.9.to[Q4_4] //the largest value in the dataset

      val old_dist = RegFile[Q4_4](nTest)
      val filler_distlabel = DistLabel(max_dist, 0)

      // find the N largest elements
      // (this runs in K log(N) for the full reduce tree i think)
      Foreach(nTest par test_par){ test_idx => 
        Sequential.Foreach(k by 1){ k_id =>
          val best = Reg[DistLabel]
        
          Reduce(best)(nTrain by 1 par sort_par){ train_idx =>
            val elem = distances(train_idx, test_idx)
            val dist = elem.dist
            val label = elem.label
            mux(dist <= old_dist(test_idx), filler_distlabel, elem)
          }{(a,b) => mux(a.dist<b.dist, a, b)}
          
          sorted_sram(k_id, test_idx) = best
          old_dist(test_idx) = best.dist
        }
      }

      // sorted output for debugging
      sortedDRAM(base :: k, base :: nTest) store sorted_sram

      val class_sram = SRAM[Char](nTest)
      val totals_sram = SRAM[LabelCount](k, nTest)

      val class_par = 1.to[Int]

      Foreach(nTest par test_par){ test_idx =>
        Foreach(classes by 1 par class_par){ c =>
          totals_sram(c, test_idx) = LabelCount(c.to[Char], 0)
        }
      }

      // find the most common element in the sorted sets
      Foreach(nTest par test_par){ test_idx =>
        Foreach(k by 1 par class_par){ kk =>
          val label_index = sorted_sram(kk, test_idx).label.to[Int]
          val label = sorted_sram(kk, test_idx).label
          val count = totals_sram(label_index, test_idx).count
          totals_sram(label_index, test_idx) = LabelCount(label, count+1)
        }
        
        val classif = Reg[LabelCount]
        Reduce(classif)(classes by 1 par class_par){ c =>
          totals_sram(c, test_idx)
        }{(a,b) => mux(a.count>b.count, a, b)}
        
        class_sram(test_idx) = classif.label
      }

      outputDRAM(base :: nTest) store class_sram
    }

    //print("dists")
    //val dists = getMatrix(distanceDRAM)
    //printMatrix(dists)

    //print("sorted")
    //val sort = getMatrix(sortedDRAM)
    //printMatrix(sort)

    print("classification")
    val out = getMem(outputDRAM)
    printArray(out)

    print("gold")
    printArray(test_labels)

    val right = out.zip(test_labels){(a,b) => if(a == b){1}else{0}}.reduce{_+_}
    println("accuracy")
    print(right)
    print("/")
    println(test_size)
    val acc = right.to[Float]/test_size.to[Float]
    println(acc)
  }
}
