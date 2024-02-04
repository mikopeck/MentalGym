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
      showingSuggestions: false,

      width: 0,
      height: 0,
      currentZoomScale: 1,

      regular_font: 14,
      selected_font: 22,
      regular_node: 8,
      selected_node: 14,
      colorScale: {
        completed_lesson: "#1f77b4",
        active_lesson: "#ff7f0e",
        completed_challenge: "#2ca02c",
        active_challenge: "#d62728",
        offered_lesson: "#9467bd",
        offered_challenge: "#8c564b",
      },
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
      this.width = window.innerWidth - 42;
      this.height = window.innerHeight - 250;

      const svg = d3
        .select("#graph")
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height);

      const graphGroup = svg.append("g");

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
        .force("center", d3.forceCenter(this.width / 2, this.height / 2));

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
        .attr("fill", (d) => this.colorScale[d.category])
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

      const vm = this; // Store a reference to the Vue instance

      const zoom = d3.zoom().on("zoom", (event) => {
        vm.currentZoomScale = event.transform.k;
        graphGroup.attr("transform", event.transform);

        node.each(function (d) {
          // Use function to get the correct 'this' for DOM element
          d3.select(this).attr(
            "r",
            d.selected
              ? vm.selected_node / vm.currentZoomScale // Use 'vm' to access Vue instance properties
              : vm.regular_node / vm.currentZoomScale
          );
        });

        labels.each(function (d) {
          const fontSize = d.selected
            ? vm.selected_font / vm.currentZoomScale
            : vm.regular_font / vm.currentZoomScale;
          d3.select(this).style("font-size", `${fontSize}px`);
        });

        labels.attr("y", (d) => d.y - 10 / vm.currentZoomScale);
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
      // Remove existing buttons if any
      d3.selectAll(".node-buttons").remove();

      // Deselect previously selected node
      if (this.selectedNode) {
        this.selectedNode.selected = false;
        d3.select(this.selectedNode.domRef)
          .transition()
          .duration(300)
          .attr("r", this.regular_node / this.currentZoomScale);
        d3.select(this.selectedNode.labelRef)
          .transition()
          .duration(300)
          .style("font-size", `${this.regular_font / this.currentZoomScale}px`);
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
              : `${this.regular_font / this.currentZoomScale}px`
          );
      }

      // If a node is selected, create and show buttons
      if (nodeData.selected) {
        this.createButtons(nodeData);
      }
    },

    createButtons(nodeData) {
      const canvasSize = { width: this.width, height: this.height };
      const buttonSize = { width: 100, height: 30 };
      const buttonGroup = d3
        .select("#graph svg")
        .append("g")
        .classed("node-buttons", true)
        .attr(
          "transform",
          `translate(0, ${canvasSize.height - buttonSize.height - 20})`
        );

      // "Go to" Button
      buttonGroup
        .append("foreignObject")
        .attr("width", buttonSize.width)
        .attr("height", buttonSize.height + 16)
        .attr("x", canvasSize.width / 2 + 16)
        .attr("y", 0)
        .append("xhtml:div")
        .attr("class", "menu-button")
        .text("Go to")
        .on("click", () => this.goToNode(nodeData));

      // "Explore" Button
      buttonGroup
        .append("foreignObject")
        .attr("width", buttonSize.width)
        .attr("height", buttonSize.height + 16)
        .attr("x", canvasSize.width / 2 - buttonSize.width - 16)
        .attr("y", 0)
        .append("xhtml:div")
        .attr("class", "menu-button explore-button")
        .text("Explore")
        .on("click", () => this.exploreNode(nodeData));
    },

    goToNode(nodeData) {
      let path;
      if (nodeData.category.includes("lesson")) {
        path = `/lesson/${nodeData.id}`;
      } else if (nodeData.category.includes("challenge")) {
        path = `/challenge/${nodeData.id}`;
      }
      console.log("Navigating to " + path);
      if (path) {
        this.$router.push(path);
      }
    },

    exploreNode(nodeData) {
      if (this.showingSuggestions) {
        d3.select("#graph svg").selectAll(".node-suggestions").remove();
        this.showingSuggestions = false;
        this.updateExploreButtonText("Explore");
      } else {
        this.updateExploreButtonText("Loading");

        fetch(`/api/explore?name=${nodeData.name}`)
          .then((response) => response.json())
          .then((data) => {
            if (data && data.suggestions) {
              this.showSuggestions(data.suggestions);
              this.showingSuggestions = true;
              this.updateExploreButtonText("Hide");
            } else {
              console.log("No suggestions received for node " + nodeData.id);
              this.updateExploreButtonText("Explore");
            }
          })
          .catch((error) => {
            console.error("Error exploring node " + nodeData.id + ": ", error);
            this.updateExploreButtonText("Explore");
          });
      }
    },

    updateExploreButtonText(newText) {
      d3.select("#graph svg").select(".explore-button").text(newText);
    },

    showSuggestions(suggestions) {
      const canvasSize = { width: this.width, height: this.height };
      const buttonSize = { width: 180, height: 50 };
      const suggestionGroup = d3
        .select("#graph svg")
        .append("g")
        .classed("node-suggestions", true)
        .attr("transform", `translate(10, 0)`);

      const buttonSpacing = 32;
      const totalHeight =
        suggestions.length * buttonSize.height +
        (suggestions.length - 1) * buttonSpacing;
      const startYPosition = canvasSize.height - 80 - totalHeight;

      suggestions.forEach((suggestion, index) => {
        const xPosition = 0;
        const yPosition =
          startYPosition + index * (buttonSize.height + buttonSpacing);

        suggestionGroup
          .append("foreignObject")
          .attr("width", buttonSize.width)
          .attr("height", buttonSize.height + 24)
          .attr("x", xPosition)
          .attr("y", yPosition)
          .append("xhtml:div")
          .attr("class", "content-button")
          .text(suggestion)
          .on("click", () => this.handleSuggestionClick(suggestion));
      });
    },
    handleSuggestionClick(suggestion) {
      console.log("Selected suggestion: " + suggestion);
      // You can add additional logic here, like navigating to the lesson or challenge
    },
  },
};
</script>

<style>
.menu-button {
  padding: 8px 16px;
  margin: 4px;
  background-color: var(--background-color-1t);
  border: 1px solid var(--text-color);
  border-radius: 8px;
  cursor: pointer;
  display: inline-block;
  backdrop-filter: blur(8px);
  transition: transform 0.1s, background-color 0.1s;
}

.menu-button:hover {
  background-color: var(--element-color-1);
}
.menu-button.selected {
  background-color: var(--element-color-1);
}

.content-button {
  padding: 0.5rem 1rem;
  background: var(--element-color-1);
  border: 2px solid var(--background-color-1t);
  border-radius: 10px;
  cursor: pointer;
  display: inline-block;
  transition: border-color 0.3s ease;
  font-size: 14px;
  text-align: center;
}

.content-button:hover {
  border-color: #6a2bc2b3;
}
</style>