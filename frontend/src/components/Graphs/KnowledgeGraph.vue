<template>
  <div v-if="loading" id="loadingCloud" class="cloud-animation">☁️</div>
  <div id="graph"></div>
</template>

<script>
import axios from "axios";
import * as d3 from "d3";
import { usePopupStore}  from "@/store/popupStore";

export default {
  name: "KnowledgeGraph",
  data() {
    return {
      loading: true,
      graphData: null,
      selectedNode: null,
      showingSuggestions: false,
      svg: null,
      zoom: null,

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
        completed_librarie: "#2ca02c",
        active_librarie: "#d62728",
        offered_lesson: "#9467bd",
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

          this.prepareGraphData();
          this.loading = false;
          const nodeName = this.$route.query.node;
          this.renderGraph(nodeName);
        })
        .catch((error) => {
          console.error("Error fetching graph data:", error);
          this.loading = false;
          const popupStore = usePopupStore();
          popupStore.showPopup("No knowledge. <a href='/library'>Go learn.</a>")
          });
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
    renderGraph(nodeName) {
      // console.log("rendering");
      this.width = window.innerWidth - 42;
      this.height = window.innerHeight - 250;
      const vm = this; // Store a reference to the Vue instance

      this.svg = d3
        .select("#graph")
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height);

      const graphGroup = this.svg.append("g");

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
        .getPropertyValue("--element-color-1")
        .trim();
      const link = graphGroup
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(this.graphData.links)
        .enter()
        .append("line")
        .attr("stroke", linkColor)
        .attr(
          "stroke-width",
          (d) => (5 * Math.sqrt(d.value)) / this.currentZoomScale
        );

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
        .attr("class", "node-text")
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

      this.zoom = d3.zoom().on("zoom", (event) => {
        vm.currentZoomScale = event.transform.k;
        graphGroup.attr("transform", event.transform);

        node.each(function (d) {
          d3.select(this).attr(
            "r",
            d.selected
              ? vm.selected_node / vm.currentZoomScale
              : vm.regular_node / vm.currentZoomScale
          );
        });

        labels.each(function (d) {
          const fontSize = d.selected
            ? vm.selected_font / vm.currentZoomScale
            : vm.regular_font / vm.currentZoomScale;
          d3.select(this).style("font-size", `${fontSize}px`);
        });

        link.each(function () {
          d3.select(this).attr(
            "stroke-width",
            (d) => (5 * Math.sqrt(d.value)) / vm.currentZoomScale
          );
        });

        labels.attr("y", (d) => d.y - 10 / vm.currentZoomScale);
      });

      this.svg.call(this.zoom);

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
          .attr("y", d.y - 10 / vm.currentZoomScale);
      }

      function dragended(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }

      // Afterstuff
      if (nodeName) {
        const nodeToSelect = this.graphData.nodes.find(
          (node) => node.name === nodeName
        );
        // console.log("Node to Select:", nodeToSelect);
        if (nodeToSelect) {
          this.selectNode(nodeToSelect, null);
        }
      }
      setTimeout(() => {
        this.zoomToNode(nodeName);
      }, 1000);
    },

    zoomToNode(nodeName) {
      if (nodeName) {
        const node = this.graphData.nodes.find(
          (n) => n.name === nodeName
        );
        if (node) {
          const zoomLevel = 4;
          const translateX = this.width / 2 - node.x * zoomLevel;
          const translateY = this.height / 2 - node.y * zoomLevel;

          // console.log(this.width / 2 + "," + this.height / 2);
          // console.log(node.x + "," + node.y);
          // console.log(translateX + "," + translateY);
          this.svg
            .transition()
            .duration(3000)
            .call(
              this.zoom.transform,
              d3.zoomIdentity.translate(translateX, translateY).scale(zoomLevel)
            );
        }
      }
    },

    selectNode(nodeData, clickedRef) {
      // Remove existing
      d3.selectAll(".node-buttons").remove();
      d3.select("#graph svg").selectAll(".node-suggestions").remove();
      this.showingSuggestions = false;

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
      if (clickedRef) {
        if (clickedRef.tagName === "circle") {
          nodeData.domRef = clickedRef;
          if (!nodeData.labelRef) {
            nodeData.labelRef = d3
              .selectAll("text")
              .nodes()
              .find((label) => d3.select(label).datum() === nodeData);
          }
        } else if (clickedRef.tagName === "text") {
          nodeData.labelRef = clickedRef;
          if (!nodeData.domRef) {
            nodeData.domRef = d3
              .selectAll("circle")
              .nodes()
              .find((node) => d3.select(node).datum() === nodeData);
          }
        }
      } else {
        // For programmatic selection, find both references if not already set
        if (!nodeData.domRef) {
          nodeData.domRef = d3
            .selectAll("circle")
            .nodes()
            .find((node) => d3.select(node).datum() === nodeData);
        }
        if (!nodeData.labelRef) {
          nodeData.labelRef = d3
            .selectAll("text")
            .nodes()
            .find((label) => d3.select(label).datum() === nodeData);
        }
      }

      // Update node style
      if (nodeData.domRef) {
        d3.select(nodeData.domRef)
          .transition()
          .duration(300)
          .attr(
            "r",
            nodeData.selected
              ? this.selected_node / this.currentZoomScale
              : this.regular_node / this.currentZoomScale
          );
      }

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
      const buttonSize = { width: 120, height: 30 };
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
        .attr("class", "knowledge-menu-button goto-button")
        .text("📖Go to")
        .on("click", () => this.goToNode(nodeData));

      // "Explore" Button
      buttonGroup
        .append("foreignObject")
        .attr("width", buttonSize.width)
        .attr("height", buttonSize.height + 16)
        .attr("x", canvasSize.width / 2 - buttonSize.width - 16)
        .attr("y", 0)
        .append("xhtml:div")
        .attr("class", "knowledge-menu-button explore-button")
        .text("🔍Explore")
        .on("click", () => this.exploreNode(nodeData));
    },

    goToNode(nodeData) {
      if (!nodeData.id) {
        this.handleSuggestionClick(nodeData.name);
        return;
      }

      let path;
      if (nodeData.category.includes("lesson")) {
        path = `/lesson/${nodeData.id}`;
      } else if (nodeData.category.includes("librar")) {
        path = `/library/${nodeData.id}`;
      }
      // console.log("Navigating to " + path);
      if (path) {
        this.$router.push(path);
      }
    },

    exploreNode(nodeData) {
      if (this.showingSuggestions) {
        d3.select("#graph svg").selectAll(".node-suggestions").remove();
        this.showingSuggestions = false;
        this.updateExploreButtonText("🔍Explore");
      } else {
        this.updateExploreButtonText("⏳Loading");

        fetch(`/api/explore?name=${nodeData.name}`)
          .then((response) => response.json())
          .then((data) => {
            if (data && data.suggestions) {
              this.showSuggestions(data.suggestions);
              this.showingSuggestions = true;
              this.updateExploreButtonText("🔽Hide");
            } else {
              this.updateExploreButtonText("🔍Explore");
            }
          })
          .catch((error) => {
            console.error("Error exploring node " + nodeData.id + ": ", error);
            this.updateExploreButtonText("🔍Explore");
          });
      }
    },

    updateExploreButtonText(newText) {
      d3.select("#graph svg").select(".explore-button").text(newText);
    },

    updateGoToButtonText(newText) {
      d3.select("#graph svg").select(".goto-button").text(newText);
    },

    showSuggestions(suggestions) {
      const canvasSize = { width: this.width, height: this.height };
      const minButtonHeight = 64;
      const buttonWidth = 200;
      const buttonSpacing = 24;

      const suggestionGroup = d3
        .select("#graph svg")
        .append("g")
        .classed("node-suggestions", true)
        .attr("transform", `translate(10, 0)`);

      let currentYPosition = canvasSize.height - 80;

      suggestions.forEach((suggestion) => {
        const estimatedLineCount = Math.ceil(suggestion.length / 25);
        const buttonHeight = Math.max(
          minButtonHeight,
          estimatedLineCount * 20 + 24
        );

        currentYPosition -= buttonHeight + buttonSpacing;

        suggestionGroup
          .append("foreignObject")
          .attr("width", buttonWidth)
          .attr("height", buttonHeight)
          .attr("x", 0)
          .attr("y", currentYPosition)
          .append("xhtml:div")
          .attr("class", "content-button")
          .style("height", `${buttonHeight}px`)
          .text(suggestion)
          .on("click", () => this.handleSuggestionClick(suggestion));
      });
    },

    async handleSuggestionClick(suggestion) {
      if (this.loading) return;

      this.loading = true;
      this.updateGoToButtonText("⏳Loading");

      try {
        // Making the POST request to the library generate route
        const libraryResponse = await axios.post("/api/library/generate", {
          topic: suggestion,
        });

        const libraryId = libraryResponse.data.library_data.id;
        this.$router.push(`/library/${libraryId}`);
      } catch (error) {
        this.loading = false;
        this.updateGoToButtonText("📖Go to");
        console.error("Error in sending request to library:", error);
      }
    },
  },
};
</script>

<style>
.knowledge-menu-button {
  text-align: center;
  margin: 0px;
  padding: 8px 16px;
  background-color: var(--background-color-1t);
  border: 1px solid var(--text-color);
  border-radius: 8px;
  cursor: pointer;
  display: inline-block;
  backdrop-filter: blur(8px);
  transition: transform 0.1s, background-color 0.1s;
}

.knowledge-menu-button:hover {
  background-color: var(--element-color-1);
}
.knowledge-menu-button.selected {
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

.node-text {
  fill: var(--text-color);
}

@keyframes cloudMove {
  0% {
    opacity: 0;
    transform: translateX(-25vw) translateY(-2vh);
  }
  25% {
    transform: translateX(-12.5vw) translateY(2vh);
  }
  50% {
    opacity: 1;
    transform: translateX(0vw) translateY(-2vh);
  }
  75% {
    transform: translateX(12.5vw) translateY(2vh);
  }
  100% {
    opacity: 0;
    transform: translateX(25vw) translateY(-2vh);
  }
}

.cloud-animation {
  font-size: 3em;
  position: absolute;
  top: 40%;
  left: 50%;
  animation: cloudMove 3s linear infinite;
}
</style>