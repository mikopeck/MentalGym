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
      const width = 800;
      const height = 600;
      let currentZoomScale = 1;

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
      };
      const regular_font = 14;
      const selected_font = 22;
      const regular_node = 8;
      const selected_node = 14;

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

      // Add a variable to store the currently selected node
      let selectedNode = null;

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
            ? selected_node / currentZoomScale
            : regular_node / currentZoomScale
        )
        .attr("fill", (d) => colorScale[d.category])
        .on("click", function (_event, d) {
          selectNode(d, this);
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
        .attr("y", (d) => d.y - 10 / currentZoomScale)
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
        .on("click", function (_event, d) {
          selectNode(d, this);
        });

      function selectNode(nodeData, clickedRef) {
        if (selectedNode) {
          // Deselect previously selected node
          selectedNode.selected = false;
          d3.select(selectedNode.domRef)
            .transition()
            .duration(300)
            .attr("r", regular_node / currentZoomScale);
          d3.select(selectedNode.labelRef)
            .transition()
            .duration(300)
            .style("font-size", `${regular_font / currentZoomScale}px`);
        }

        // Toggle the selection state
        nodeData.selected = !nodeData.selected;
        selectedNode = nodeData.selected ? nodeData : null;

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
              ? selected_node / currentZoomScale
              : regular_node / currentZoomScale
          );

        // Update label style
        if (nodeData.labelRef) {
          d3.select(nodeData.labelRef)
            .transition()
            .duration(300)
            .style(
              "font-size",
              nodeData.selected
                ? `${selected_font / currentZoomScale}px`
                : `${regular_font / currentZoomScale}px`
            );
        }
      }

      const zoom = d3.zoom().on("zoom", (event) => {
        currentZoomScale = event.transform.k;
        graphGroup.attr("transform", event.transform);

        node.each(function (d) {
          d3.select(this).attr(
            "r",
            d.selected
              ? selected_node / currentZoomScale
              : regular_node / currentZoomScale
          );
        });

        labels.each(function (d) {
          const fontSize = d.selected
            ? selected_font / currentZoomScale
            : regular_font / currentZoomScale;
          d3.select(this).style("font-size", `${fontSize}px`);
        });

        labels.attr("y", (d) => d.y - 10 / currentZoomScale);
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
          .attr("y", (d) => d.y - 10 / currentZoomScale);
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
          .attr("y", d.y - 10 / currentZoomScale);
      }

      function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
    },
  },
};
</script>

<style>
</style>
