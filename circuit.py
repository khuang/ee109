from typing import List, Dict

from block import Block, Node

import math
from graphviz import Digraph

class Circuit:
    """An analog circuit composed of blocks."""
    def __init__(self, *blocks: List[Block]) -> None:
        self.blocks = blocks
        self.block_index = 0
        self.elapsed_time = 0
        self.steps_taken = 0
        self.max_tau = 0
        self.min_bandwidth = 0
        self.area = 0
        self.power = 0
        self.nodes = []
        self.con_vals = []

        nodes = []
        for block in self.blocks:
            nodes.extend(block.inputs)
            nodes.extend(block.outputs)
        self.nodes = list(set(nodes))
        print('owiehfoiwehfiowehfiowehiowhfoiwhfoiwhfoiwhfiowehfowhfoiwehfoiwhefo')
        print(self.nodes)

    def simulate(self, nodes: List[Node], steps: int=100, target_node: Node=None,
                 target: float=None, error: float=0.01, desired_time: float=1.0,
                 step_size: float=1.0, force_immediate: bool=False,
                 force_sequential: bool=False, settled_error: float=0) -> List[Dict[str, float]]:
        """Simulates the circuit, recording the values of nodes.

        Parameters
        ----------
        nodes: list
            list of nodes to simulate
        steps: int
            number of steps to simulate
        target_node: Node
            optional node to watch to get target within multiplicative factor of error
        error: float
            ???
        desired_time: float
            time in which the whole circuit should converge
        step_size: float
            fraction of the way we want the fastest block to go to its
            target before declaring a new timestep
        force_immediate: bool
            ???
        force_sequential: bool
            ???
        settled_error: float
            ???

        Returns
        -------
        node_vals: list
            a list of name, value pairs for each node
        """

        # Get node values
        node_vals = [[(node.name, node.value) for node in nodes]]#[{node.name: node.value for node in nodes}]

        # Find maximum bandwidth for blocks
        max_bandwidth = max([block.bandwidth for block in self.blocks])

        # Simulate step by step
        # Store times when we enter the convergence bounds
        in_bounds = False
        step_in_bounds = None
        time_in_bounds = None
        converged = False
        con_vals = []
        self.con_vals = [];
        self.steps_taken = 0;
        self.elapsed_time = 0;
        for step_cnt in range(steps):
            old_vals = [(node.name, node.value) for node in nodes]
            self.elapsed_time += self.step(step_size, max_bandwidth,
                                           force_immediate=force_immediate,
                                           force_sequential=force_sequential)
            self.steps_taken += 1
            new_vals = [(node.name, node.value) for node in nodes]
            node_vals.append(new_vals)#{node.name: node.value for node in nodes})#

            # End once we've reached our target within error bounds
            if(target_node is not None and target is not None):
                bounded = True
                for t in range(len(target_node)):
                    t_n = target_node[t]
                    tar = target[t]
                    lower_bound = abs(tar * (1.0 - error))
                    upper_bound = abs(tar * (1.0 + error))
                    if not (lower_bound <= abs(t_n.value) <= upper_bound):
                        bounded = False
                        in_bounds = False
                if bounded and not in_bounds:
                    in_bounds = True
                    step_in_bounds = step_cnt
                    time_in_bounds = self.elapsed_time
                    con_vals = [(node.name, node.value) for node in nodes]
                    break

            # End if every node is settled within settled_percent
            scaled_error = settled_error * step_size #should use min_step_size, leaving for now
            if not converged and step_cnt > 100: #fix to things being all 0 at first
                converged = True
                for i in range(len(old_vals)):
                    lower_bound = abs(old_vals[i][1]) - scaled_error
                    upper_bound = abs(old_vals[i][1]) + scaled_error
                    if not (lower_bound <= abs(new_vals[i][1]) <= upper_bound):
                        converged = False
                if converged:
                    step_in_bounds = step_cnt
                    time_in_bounds = self.elapsed_time
                    con_vals = [(node.name, node.value) for node in nodes]
                    break

        # Find the last time we converged
        if(target_node is not None and target is not None):
            if in_bounds:
                self.steps_taken = step_in_bounds
                self.elapsed_time = time_in_bounds
                self.con_vals = con_vals

        if(converged):
            self.steps_taken = step_in_bounds
            self.elapsed_time = time_in_bounds
            self.con_vals = con_vals

        # Calculate metrics
        if step_size != 1.0:
            # Find the bandwidth we need to satisfy the desired time
            des_step_time = desired_time / self.steps_taken
            self.max_tau = des_step_time / math.log(1.0 / (1.0 - step_size))
            self.min_bandwidth = 1.0 / self.max_tau

        for block in self.blocks:
            # Scale all blocks based on the min and max bandwidths
            self.power += self.min_bandwidth * (block.power / max_bandwidth)
            self.area += self.min_bandwidth * (block.area / max_bandwidth)

        return node_vals

    def step(self, step_size, max_bandwidth, force_immediate=False,
             force_sequential=False) -> None:
        """Step the simulation one step forward in time.

        Parameters
        ----------
        step_size: float
            ???
        max_bandwidth: float
            ???
        force_immediate: bool
            ???
        force_sequential: bool
            ???

        Returns
        -------
        settle_time: float
            the time it took the whole circuit to settle
        """
        max_time = 0.0

        # Ignoring the step parameter, still works
        # Update every block, getting settling times
        settle_times = []
        for block in self.blocks:
            t_settle = block.run(
                step_size, max_bandwidth, force_immediate=force_immediate,
                force_sequential=force_sequential)
            settle_times.append(t_settle)

        # Update all the nodes if they don't update immediately
        if not force_sequential:
            for node in self.nodes:
                node.step()
        return max(settle_times)

    @staticmethod
    def get_node_text(node, show_node_id=False):
        """Helper method to get the text for nodes in plots.

        Parameters
        ----------
        node: Node
            the node to get the name for
        show_node_id: bool
            whether or not to include the node id"""
        if show_node_id:
            return f'{node.name} ({id(node)})'
        else:
            return node.name

    def draw(self, show_node_ids=True):
        """Generates a graphviz plot of the circuit.

        Parameters
        ----------
        show_node_ids: bool
            whether or not to show the node ids on the plot
        """

        dot = Digraph(comment='Circuit')

        dot.node("inputs", "inputs", color="red")
        dot.node("outputs", "outputs", color="blue")

        for block in self.blocks:
            dot.node(str(id(block)), str(type(block)))

        for node in self.nodes:
            is_input = True
            for block_out in self.blocks:
                if node in block_out.outputs:
                    is_input = False
                    is_output = True
                    node_name = self.get_node_text(
                        node, show_node_id=show_node_ids)
                    for block_in in self.blocks:
                        if node in block_in.inputs:
                            is_output = False
                            dot.edge(str(id(block_out)), str(id(block_in)),
                                     label=node_name)
                    if is_output:
                        dot.edge(str(id(block_out)), "outputs",
                                 label=node_name)
            if is_input:
                for block_in in self.blocks:
                    if node in block_in.inputs:
                        node_name = self.get_node_text(
                            node, show_node_id=show_node_ids)
                        dot.edge("inputs", str(id(block_in)),
                                 label=node_name)

        dot.render('test_output/circ.gv')


def get_node_text(node, show_node_id=False):
    """Helper method to get the text for nodes in plots.

    Parameters
    ----------
    node: Node
        the node to get the name for
    show_node_id: bool
        whether or not to include the node id"""
    if show_node_id:
        return f'{node.name} ({id(node)})'
    else:
        return node.name


def draw_circuit(circuit, show_node_ids=True):
    """Generates a graphviz plot of the circuit.

    Parameters
    ----------
    show_node_ids: bool
        whether or not to show the node ids on the plot
    """

    dot = Digraph(comment='Circuit')

    dot.node("inputs", "inputs", color="red")
    dot.node("outputs", "outputs", color="blue")

    for block in circuit.blocks:
        dot.node(str(id(block)), str(type(block)))

    for node in circuit.all_nodes:
        is_input = True
        for block_out in circuit.blocks:
            if node in block_out.outputs:
                is_input = False
                is_output = True
                node_name = get_node_text(
                    node, show_node_id=show_node_ids)
                for block_in in circuit.blocks:
                    if node in block_in.inputs:
                        is_output = False
                        dot.edge(str(id(block_out)), str(id(block_in)),
                                 label=node_name)
                if is_output:
                    dot.edge(str(id(block_out)), "outputs",
                             label=node_name)
        if is_input:
            for block_in in circuit.blocks:
                if node in block_in.inputs:
                    node_name = get_node_text(
                        node, show_node_id=show_node_ids)
                    dot.edge("inputs", str(id(block_in)),
                             label=node_name)

    dot.render('test_output/circ.gv')
