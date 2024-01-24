<template>
  <div id="graph"></div>
</template>

<script>
import * as d3 from "d3";

export default {
  name: "KnowledgeGraph",
  data() {
    return {
      graphData: null,
      selectedNode: null,
      regular_font: 14,
      selected_font: 22,
      regular_node: 8,
      selected_node: 14,
      currentZoomScale: 1,
    };
  },
  mounted() {
    this.fetchGraphData();
  },
  methods: {
    fetchGraphData() {
      fetch("/api/knowledge-net")
        .then((response) => response.json())
        .then((data) => {
          this.graphData = data.data;
          console.log(data);
          console.log(this.graphData);

          this.prepareGraphData();
          this.renderGraph();
        })
        .catch((error) => console.error("Error fetching graph data:", error));
    },
    prepareGraphData() {
      // Transform edges to D3 format
      this.graphData.links = this.graphData.edges.map((edge) => {
        return {
          source: this.graphData.nodes.findIndex(
            (node) => node.name === edge.from
          ),
          target: this.graphData.nodes.findIndex(
            (node) => node.name === edge.to
          ),
          value: edge.similarity,
        };
      });
    },
    renderGraph() {
      console.log("rendering");
      const width = window.innerWidth * 0.85;
      const height = window.innerHeight * 0.6;

      const svg = d3
        .select("#graph")
        .append("svg")
        .attr("width", width)
        .attr("height", height);

      const graphGroup = svg.append("g");

      const colorScale = {
        completed_lesson: "#1f77b4",
        active_lesson: "#ff7f0e",
        completed_challenge: "#2ca02c",
        active_challenge: "#d62728",
        offered_lesson: "#9467bd",
        offered_challenge: "#8c564b",
      };

      // Create the force simulation
      const simulation = d3
        .forceSimulation(this.graphData.nodes)
        .force(
          "link",
          d3
            .forceLink(this.graphData.links)
            .id((d) => d.index)
            .strength((d) => d.value)
        )
        .force("charge", d3.forceManyBody())
        .force("center", d3.forceCenter(width / 2, height / 2));

      // Render links
      const linkColor = getComputedStyle(document.documentElement)
        .getPropertyValue("--highlight-color")
        .trim();
      const link = graphGroup
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(this.graphData.links)
        .enter()
        .append("line")
        .attr("stroke", linkColor)
        .attr("stroke-width", (d) => Math.sqrt(d.value));

      // Render nodes
      const node = graphGroup
        .append("g")
        .attr("class", "nodes")
        .selectAll("circle")
        .data(this.graphData.nodes)
        .enter()
        .append("circle")
        .attr("r", (d) =>
          d.selected
            ? this.selected_node / this.currentZoomScale
            : this.regular_node / this.currentZoomScale
        )
        .attr("fill", (d) => colorScale[d.category])
        .on("click", (_event, d) => {
          this.selectNode(d, _event.currentTarget);
        })
        .call(
          d3
            .drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)
        );

      // Render labels
      const labels = graphGroup
        .append("g")
        .attr("class", "labels")
        .selectAll("text")
        .data(this.graphData.nodes)
        .enter()
        .append("text")
        .text((d) => d.name)
        .attr("x", (d) => d.x)
        .attr("y", (d) => d.y - 10 / this.currentZoomScale)
        .attr("text-anchor", "middle")
        .style(
          "fill",
          getComputedStyle(document.documentElement)
            .getPropertyValue("--text-color")
            .trim()
        )
        .style("font-size", `14px`)
        .call(
          d3
            .drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)
        )
        .on("click", (_event, d) => {
          this.selectNode(d, _event.currentTarget);
        });

      const zoom = d3.zoom().on("zoom", (event) => {
        this.currentZoomScale = event.transform.k;
        graphGroup.attr("transform", event.transform);

        node.each(function (d) {
          d3.select(this).attr(
            "r",
            d.selected
              ? this.selected_node / this.currentZoomScale
              : this.regular_node / this.currentZoomScale
          );
        });

        labels.each(function (d) {
          const fontSize = d.selected
            ? this.selected_font / this.currentZoomScale
            : this.regular_font  / this.currentZoomScale;
          d3.select(this).style("font-size", `${fontSize}px`);
        });

        labels.attr("y", (d) => d.y - 10 / this.currentZoomScale);
      });
      svg.call(zoom);

      // Update positions on each tick
      simulation.on("tick", () => {
        link
          .attr("x1", (d) => d.source.x)
          .attr("y1", (d) => d.source.y)
          .attr("x2", (d) => d.target.x)
          .attr("y2", (d) => d.target.y);

        node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
        labels
          .attr("x", (d) => d.x)
          .attr("y", (d) => d.y - 10 / this.currentZoomScale);
      });

      function dragstarted(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
        labels
          .filter((ld) => ld === d)
          .attr("x", d.x)
          .attr("y", d.y - 10 / this.currentZoomScale);
      }

      function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
    },
    selectNode(nodeData, clickedRef) {
      if (this.selectedNode) {
        if (this.selectedNode === nodeData && nodeData.id) {
          let path;
          if (nodeData.category.includes("lesson")) {
            path = `/lesson/${nodeData.id}`;
          } else if (nodeData.category.includes("challenge")) {
            path = `/challenge/${nodeData.id}`;
          }
          console.log("pathins" + path);
          if (path) {
            this.$router.push(path);
          }
          return;
        }

        // Deselect previously selected node
        this.selectedNode.selected = false;
        d3.select(this.selectedNode.domRef)
          .transition()
          .duration(300)
          .attr("r", this.regular_node / this.currentZoomScale);
        d3.select(this.selectedNode.labelRef)
          .transition()
          .duration(300)
          .style("font-size", `${this.regular_font  / this.currentZoomScale}px`);
      }

      // Toggle the selection state
      nodeData.selected = !nodeData.selected;
      this.selectedNode = nodeData.selected ? nodeData : null;

      // Update node and label references if necessary
      if (clickedRef.tagName === "circle") {
        nodeData.domRef = clickedRef;
        // Find the corresponding label element if not already stored
        if (!nodeData.labelRef) {
          nodeData.labelRef = d3
            .selectAll("text")
            .nodes()
            .find((label) => d3.select(label).datum() === nodeData);
        }
      } else if (clickedRef.tagName === "text") {
        nodeData.labelRef = clickedRef;
        // Find the corresponding node element if not already stored
        if (!nodeData.domRef) {
          nodeData.domRef = d3
            .selectAll("circle")
            .nodes()
            .find((node) => d3.select(node).datum() === nodeData);
        }
      }

      // Update node style
      d3.select(nodeData.domRef)
        .transition()
        .duration(300)
        .attr(
          "r",
          nodeData.selected
            ? this.selected_node / this.currentZoomScale
            : this.regular_node / this.currentZoomScale
        );

      // Update label style
      if (nodeData.labelRef) {
        d3.select(nodeData.labelRef)
          .transition()
          .duration(300)
          .style(
            "font-size",
            nodeData.selected
              ? `${this.selected_font / this.currentZoomScale}px`
              : `${this.regular_font  / this.currentZoomScale}px`
          );
      }
    },
  },
};
</script>

<style>
</style>
