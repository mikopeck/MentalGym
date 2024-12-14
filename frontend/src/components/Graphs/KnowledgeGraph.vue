<template>
  <div>
    <div v-if="loading" id="loadingCloud" class="cloud-animation">☁️</div>
    <div id="graph"></div>
  </div>
</template>

<script>
import axios from "axios";
import * as d3 from "d3";
import { usePopupStore } from "@/store/popupStore";

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
      baseCollisionRadius: 70,
      simulation: null,
      link: null,
      node: null,
      graphGroup: null,
    };
  },
  mounted() {
    this.fetchGraphData();
  },
  methods: {
    async fetchGraphData() {
      try {
        const response = await fetch("/api/knowledge-net");
        const data = await response.json();
        this.graphData = data.data;
        this.prepareGraphData();
        this.loading = false;

        const nodeName = this.$route.query.node;
        this.renderGraph(nodeName);
      } catch (error) {
        console.error("Error fetching graph data:", error);
        this.loading = false;
        const popupStore = usePopupStore();
        popupStore.showPopup("No knowledge. <a href='/library'>Go learn.</a>");
      }
    },

    prepareGraphData() {
      // Convert custom edges into D3 link format
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
      this.width = window.innerWidth - 42;
      this.height = window.innerHeight - 250;
      const vm = this;

      this.svg = d3
        .select("#graph")
        .append("svg")
        .attr("width", this.width)
        .attr("height", this.height);

      this.graphGroup = this.svg.append("g");

      this.simulation = d3
        .forceSimulation(this.graphData.nodes)
        .force(
          "link",
          d3
            .forceLink(this.graphData.links)
            .id((d) => d.index)
            .strength((d) => d.value)
        )
        .force("charge", d3.forceManyBody().strength(-30))
        .force("collide", d3.forceCollide(this.baseCollisionRadius))
        .force("center", d3.forceCenter(this.width / 2, this.height / 2));

      const linkColor = getComputedStyle(document.documentElement)
        .getPropertyValue("--element-color-1")
        .trim();

      // Draw Links
      this.link = this.graphGroup
        .append("g")
        .attr("class", "links")
        .selectAll("line")
        .data(this.graphData.links)
        .enter()
        .append("line")
        .attr("stroke", linkColor)
        .attr("stroke-width", (d) => 5 * Math.sqrt(d.value));

      // Draw Nodes
      this.node = this.graphGroup.append("g").attr("class", "nodes").selectAll("foreignObject")
        .data(this.graphData.nodes)
        .enter()
        .append("foreignObject")
        .attr("width", 240)
        .attr("height", 120)
        .on("click", (event, d) => {
          this.selectNode(d);
        })
        .call(
          d3
            .drag()
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended)
        );

      // Create node buttons
      this.node
        .append("xhtml:button")
        .attr("class", "content-button")
        .classed("completed-button", (d) => d.category.includes("completed"))
        .html((d) => {
          const emoji = this.getEmojiForContentType(d.category);
          const contentName = this.removeEmoji(d.name);
          const extractedEmoji = this.extractEmoji(d.name);
          return `
            ${emoji ? `<span class="emoji-indicator">${emoji}</span>` : ""}
            <span class="content-name">${contentName}</span>
            ${
              extractedEmoji
                ? `<span class="emoji-indicator">${extractedEmoji}</span>`
                : ""
            }
          `;
        });

      // Zoom behavior
      this.zoom = d3.zoom().on("zoom", (event) => {
        vm.currentZoomScale = event.transform.k;
        vm.graphGroup.attr("transform", event.transform);

        vm.simulation.force(
          "collide",
          d3.forceCollide(vm.baseCollisionRadius * vm.currentZoomScale)
        );
        vm.simulation.alpha(0.02).restart();
      });
      this.svg.call(this.zoom);

      // If the click is not on a node, deselect the current node.
      this.svg.on("click", (event) => {
        if (
          !d3.select(event.target).classed("content-name") &&
          !d3.select(event.target).classed("content-button") &&
          !d3.select(event.target).classed("knowledge-menu-button")
        ) {
          this.deselectNode();
        }
      });

      this.simulation.on("tick", () => {
        this.link
          .attr("x1", (d) => d.source.x)
          .attr("y1", (d) => d.source.y)
          .attr("x2", (d) => d.target.x)
          .attr("y2", (d) => d.target.y);

        this.node.attr("x", (d) => d.x - 110).attr("y", (d) => d.y - 30);
      });

      // Initial focus if nodeName is provided
      if (nodeName) {
        const nodeToSelect = this.graphData.nodes.find(
          (n) => n.name === nodeName
        );
        if (nodeToSelect) {
          setTimeout(() => {
            this.selectNode(nodeToSelect);
          }, 1200);
        }
      }

      this.simulation.alpha(1).restart();
      setTimeout(() => {
        this.simulation.stop();
      }, 1200);

      function dragstarted(event, d) {
        if (!event.active) vm.simulation.alphaTarget(0.2).restart();
        d.fx = d.x;
        d.fy = d.y;
      }

      function dragged(event, d) {
        d.fx = event.x;
        d.fy = event.y;
      }

      function dragended(event, d) {
        if (!event.active) vm.simulation.alphaTarget(0);
        d.fx = null;
        d.fy = null;
      }
    },

    deselectNode() {
      d3.select("#graph svg").selectAll(".node-suggestions").remove();
      d3.select("#graph svg").selectAll(".knowledge-menu-button").remove();
      this.showingSuggestions = false;
      this.updateExploreButtonText("🔍Explore");
      if (this.selectedNode && this.selectedNode.domRef) {
        d3.select(this.selectedNode.domRef).classed("selected", false);
      }
    },

    selectNode(nodeData) {
      this.deselectNode();

      if (this.selectedNode === nodeData) {
        this.selectedNode = null;
      } else {
        this.selectedNode = nodeData;
      }

      const allNodes = d3.selectAll(".content-button").nodes();
      nodeData.domRef = allNodes.find(
        (el) => d3.select(el).datum() === nodeData
      );

      if (this.selectedNode && nodeData.domRef) {
        d3.select(nodeData.domRef).classed("selected", true);

        // Center and zoom into the selected node
        const zoomLevel = 2;
        const translateX = this.width / 2 - nodeData.x * zoomLevel;
        const translateY = this.height / 2 - nodeData.y * zoomLevel;

        this.svg
          .transition()
          .duration(1000)
          .call(
            this.zoom.transform,
            d3.zoomIdentity.translate(translateX, translateY).scale(zoomLevel)
          );

        this.createActionButtons(nodeData);
      }
    },

    getEmojiForContentType(contentType) {
      switch (contentType) {
        case "lesson":
        case "completed_lesson":
          return "📖";
        case "completed_librarie":
        case "library":
          return "🏛️";
        case "suggestion":
        default:
          return "☁️";
      }
    },

    extractEmoji(content) {
      const emojiRegex =
        /[\u{1F600}-\u{1F64F}\u{1F300}-\u{1F5FF}\u{1F680}-\u{1F6FF}\u{1F700}-\u{1F77F}\u{1F780}-\u{1F7FF}\u{1F800}-\u{1F8FF}\u{1F900}-\u{1F9FF}\u{1FA00}-\u{1FA6F}\u{1FA70}-\u{1FAFF}\u{2600}-\u{26FF}\u{2700}-\u{27BF}]/u;
      const match = content.match(emojiRegex);
      return match ? match[0] : "";
    },

    removeEmoji(content) {
      const emoji = this.extractEmoji(content);
      return content.replace(emoji, "").trim();
    },

    createActionButtons(nodeData) {
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

      if (path) {
        this.$router.push(path);
      }
    },

    async exploreNode(nodeData) {
      if (this.showingSuggestions) {
        // Hide suggestions if already showing
        this.removeSuggestionsNodes();
        this.showingSuggestions = false;
        this.updateExploreButtonText("🔍Explore");
      } else {
        this.updateExploreButtonText("⏳Loading");
        try {
          const response = await fetch(`/api/explore?name=${nodeData.name}`);
          const data = await response.json();

          if (data && data.suggestions) {
            this.addSuggestionsToGraph(data.suggestions, nodeData);
            this.showingSuggestions = true;
            this.updateExploreButtonText("🔽Hide");
          } else {
            this.updateExploreButtonText("🔍Explore");
          }
        } catch (error) {
          console.error("Error exploring node:", error);
          this.updateExploreButtonText("🔍Explore");
        }
      }
    },

    updateExploreButtonText(newText) {
      d3.select("#graph svg").select(".explore-button").text(newText);
    },

    updateGoToButtonText(newText) {
      d3.select("#graph svg").select(".goto-button").text(newText);
    },

    // Add suggestion nodes to graph and connect them to the selected node
    addSuggestionsToGraph(suggestions, nodeData) {
      const originIndex = this.graphData.nodes.indexOf(nodeData);
      // Create new nodes for suggestions
      suggestions.forEach((suggestion) => {
        const newNode = {
          name: suggestion,
          category: "suggestion"
        };
        this.graphData.nodes.push(newNode);
        const newNodeIndex = this.graphData.nodes.length - 1;

        this.graphData.links.push({
          source: originIndex,
          target: newNodeIndex,
          value: 0.1,
        });
      });

      // Update the simulation and re-draw
      this.updateGraph();
      // Restart simulation with slight alpha
      this.simulation.alpha(0.1).restart();
    },

    removeSuggestionsNodes() {
      // Remove all suggestion nodes from graphData
      // This is optional; if we want to actually remove them, we need logic here.
      // For now, we won't remove them, just won't show them again. 
      // If needed, implement filtering out "suggestion" category nodes here.
    },

    updateGraph() {
      const linkColor = getComputedStyle(document.documentElement)
        .getPropertyValue("--element-color-1")
        .trim();

      // Update links
      this.link = this.graphGroup.select(".links").selectAll("line")
        .data(this.graphData.links, (d) => `${d.source.index}-${d.target.index}`);

      this.link.exit().remove();

      this.link = this.link
        .enter()
        .append("line")
        .attr("stroke", linkColor)
        .attr("stroke-width", (d) => 5 * Math.sqrt(d.value))
        .merge(this.link);

      // Update nodes
      const nodeGroup = this.graphGroup.select(".nodes").selectAll("foreignObject")
        .data(this.graphData.nodes, (d) => d.name);

      nodeGroup.exit().remove();

      const nodeEnter = nodeGroup
        .enter()
        .append("foreignObject")
        .attr("width", 240)
        .attr("height", 120)
        .on("click", (event, d) => {
          this.selectNode(d);
        })
        .call(
          d3
            .drag()
            .on("start", (event, d) => {
              if (!event.active) this.simulation.alphaTarget(0.2).restart();
              d.fx = d.x;
              d.fy = d.y;
            })
            .on("drag", (event, d) => {
              d.fx = event.x;
              d.fy = event.y;
            })
            .on("end", (event, d) => {
              if (!event.active) this.simulation.alphaTarget(0);
              d.fx = null;
              d.fy = null;
            })
        );

      nodeEnter
        .append("xhtml:button")
        .attr("class", "content-button")
        .classed("completed-button", (d) => d.category && d.category.includes("completed"))
        .html((d) => {
          const emoji = this.getEmojiForContentType(d.category);
          const contentName = this.removeEmoji(d.name);
          const extractedEmoji = this.extractEmoji(d.name);
          return `
            ${emoji ? `<span class="emoji-indicator">${emoji}</span>` : ""}
            <span class="content-name">${contentName}</span>
            ${
              extractedEmoji
                ? `<span class="emoji-indicator">${extractedEmoji}</span>`
                : ""
            }
          `;
        });

      this.node = nodeEnter.merge(nodeGroup);

      // Update simulation with new data
      this.simulation.nodes(this.graphData.nodes);
      this.simulation.force("link").links(this.graphData.links);
    },

    async handleSuggestionClick(suggestion) {
      if (this.loading) return;

      this.loading = true;
      this.updateGoToButtonText("⏳Loading");

      try {
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
  transition: transform 0.1s, background-color 0.1s;
}

.knowledge-menu-button:hover {
  background-color: var(--element-color-1);
}

.content-button {
  display: flex;
  flex-direction: row;
  align-items: center;
  justify-content: center;
  padding: 0.5rem 1rem;
  background: var(--element-color-1);
  border: 2px solid var(--background-color-1t);
  border-radius: 8px;
  cursor: pointer;
  text-align: center;
  position: relative;
  transition: all 0.3s ease;
}

.selected {
  border-color: var(--highlight-color);
}

.content-name {
  padding: 8px;
}

.content-button .emoji-indicator {
  font-size: 1.5rem;
}

.content-button:hover {
  border-color: var(--element-color-2);
}

.completed-button {
  border-color:  var(--gold-color);
  opacity: 0.9;
  position: relative;
}

.completed-button::after {
  content: "✓";
  color: #50c878;
  font-weight: bold;
  font-size: 1.2rem;
  position: absolute;
  right: 10px;
  top: 80%;
  transform: translateY(-50%);
}

.cloud-animation {
  font-size: 3em;
  position: absolute;
  top: 40%;
  left: 50%;
  animation: cloudMove 3s linear infinite;
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
</style>
