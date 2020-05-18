import Utils.toSpatialIntArray
import spatial.dsl._
import scala.math.abs


@spatial object KNN extends SpatialApp {
  def main(args: Array[String]): Unit = {

    val k = 2
    val test_size = 2
    val train_size = 10
    val v_len = 2
    
    //dummy data
    val test_set = (0::test_size, 0::v_len){(i,j) => i.to[Float]}
    val train_set = (0::train_size, 0::v_len){(i,j) => (10 - i).to[Float]}
    val train_labels = scala.Array(1,2)

    print("test")
    printMatrix(test_set)
    print("train")
    printMatrix(train_set)

    val dTrain = DRAM[Float](train_size.to[Int], v_len.to[Int])
    val dTest = DRAM[Float](test_size.to[Int], v_len.to[Int])

    val classification = ArgOut[Int]

    setMem(dTrain, train_set)
    setMem(dTest, test_set)

    // temp test vars
    val outputDRAM = DRAM[Float](train_size.to[Int], test_size.to[Int])
    val sortedDRAM = DRAM[Float](k.to[Int], test_size.to[Int])

    Accel {
      val nTrain = 10.to[Int]
      val nTest = 2.to[Int]
      val vLen = 2.to[Int]
      val k = 2.to[Int]

      val base = 0.to[Int]
      val test_par = 1.to[Int]
      val train_par = 1.to[Int]
      val dist_par = 1.to[Int]
      val load_par = 1.to[Int]
      val step = 1.to[Int]

      val test_sram = SRAM[Float](nTest, vLen)
      val train_sram = SRAM[Float](nTrain, vLen)
      val distances = SRAM[Float](nTrain, nTest)

      test_sram load dTest(base :: nTest par load_par, base :: vLen)
      train_sram load dTrain(base :: nTrain par load_par, base :: vLen)

      Foreach(nTest by step par test_par){ test_idx =>
        Foreach(nTrain by step par train_par){ train_idx =>
          val distance = Reg[Float](0)
          Reduce(distance)(vLen by 1 par dist_par){ i =>
            val pos = test_sram(test_idx, i) - train_sram(train_idx, i)
            val neg = train_sram(train_idx, i) - test_sram(test_idx, i)
            val abs = mux(pos > neg, pos, neg) //jank absolute value function
            //println("abs")
            //println(abs)
            abs
          }{_+_} //this is the manhattan distance
          //println("dist")
          //println(distance)
          distances(train_idx, test_idx) = distance
        }
      }

      outputDRAM(base :: nTrain, base :: nTest) store distances

      val sorted_sram = SRAM[Float](k, nTest)
      val sorted_labels_sram = SRAM[Float](k, nTest)

      val sort_par = 1.to[Int]
      val max_dist = 100.to[Float]

      val old_dist = RegFile[Float](nTest)

      Foreach(nTest par test_par){ test_idx => 
        //old_dist(test_idx) = 0.to[Int]
        Sequential.Foreach(k by 1){ k_id =>
          val best = Reg[Float](0)
        
          Reduce(best)(nTrain by 1 par sort_par){ train_idx =>
            val dist = distances(train_idx, test_idx)
            mux(dist <= old_dist(test_idx), max_dist, dist)
          }{(a,b) => mux(a<b, a, b)}
          
          sorted_sram(k_id, test_idx) = best
          old_dist(test_idx) = best
        }
      }

      sortedDRAM(base :: k, base :: nTest) store sorted_sram
    }

    print("dists")
    val dists = getMatrix(outputDRAM)
    printMatrix(dists)

    print("sorted")
    val sort = getMatrix(sortedDRAM)
    printMatrix(sort)
  }
}
