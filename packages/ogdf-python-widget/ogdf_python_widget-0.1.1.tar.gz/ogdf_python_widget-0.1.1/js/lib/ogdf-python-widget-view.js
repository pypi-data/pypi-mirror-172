let widgets = require('@jupyter-widgets/base');
let _ = require('lodash');
let d3 = require("d3");
let c = require('./graph-element-constructer')
require("./style.css");

// See widget.py for the kernel counterpart to this file.


// Custom Model. Custom widgets models must at least provide default values
// for model attributes, including
//
//  - `_view_name`
//  - `_view_module`
//  - `_view_module_version`
//
//  - `_model_name`
//  - `_model_module`
//  - `_model_module_version`
//
//  when different from the base class.

// When serializing the entire widget state for embedding, only values that
// differ from the defaults will be specified.
let WidgetModel = widgets.DOMWidgetModel.extend({
    defaults: _.extend(widgets.DOMWidgetModel.prototype.defaults(), {
        _model_name: 'WidgetModel',
        _view_name: 'WidgetView',
        _model_module: 'ogdf-python-widget',
        _view_module: 'ogdf-python-widget',
        _model_module_version: '0.1.0',
        _view_module_version: '0.1.0',
        width: 960,
        height: 540,
        x_pos: 0,
        y_pos: 0,
        zoom: 1,
        click_thickness: 10,
        animation_duration: 1000,
        force_config: null,
        rescale_on_resize: true,
    })
});

// Custom View. Renders the widget model.
let WidgetView = widgets.DOMWidgetView.extend({
    initialize: function (parameters) {
        WidgetView.__super__.initialize.call(this, parameters);

        this.isNodeMovementEnabled = this.model.get("node_movement_enabled")

        //only for internal use
        this.isTransformCallbackAllowed = true

        this.forceDirected = false

        this.clickThickness = this.model.get("click_thickness")
        this.animationDuration = this.model.get("animation_duration")
        this.gridSize = this.model.get('grid_size');

        this.nodes = []
        this.links = []
        this.clusters = []
        this.virtualLinks = []

        this.width = this.model.get('width')
        this.height = this.model.get('height')

        this.model.on('msg:custom', this.handle_msg.bind(this));

        this.model.on('change:x_pos', this.transformCallbackCheck, this);
        this.model.on('change:y_pos', this.transformCallbackCheck, this);
        this.model.on('change:zoom', this.transformCallbackCheck, this);

        this.model.on('change:width', this.svgSizeChanged, this)
        this.model.on('change:height', this.svgSizeChanged, this)

        this.model.on('change:click_thickness', this.clickThicknessChanged, this)

        this.model.on('change:animation_duration', this.animationDurationChanged, this)

        this.model.on('change:grid_size', this.gridSizeChanged, this)

        this.model.on('change:force_config', this.forceConfigChanged, this)

        this.model.on('change:node_movement_enabled', this.nodeMovementChanged, this)

        this.ticksSinceSync = 0

        this.send({"code": "widgetReady"})
    },

    handle_msg: function (msg) {
        if (msg.code === 'clearGraph') {
            this.clearGraph()
        } else if (msg.code === 'initGraph') {
            this.links = msg.links
            this.nodes = msg.nodes
            this.clusters = msg.clusters
            this.rootClusterId = msg.rootClusterId
            this.isClusterGraph = this.rootClusterId !== '-1'
            this.isSPQRTree = msg.SPQRtree
            if (this.isSPQRTree)
                this.virtualLinks = msg.virtualLinks
            this.render()
            this.forceConfigChanged()
        } else if (msg.code === 'nodeAdded') {
            this.addNode(msg.data)
        } else if (msg.code === 'linkAdded') {
            this.addLink(msg.data)
        } else if (msg.code === 'addClusterById') {
            this.addCluster(msg.data)
            console.log(this.clusters)
        } else if (msg.code === 'deleteNodeById') {
            this.deleteNodeById(msg.data)
        } else if (msg.code === 'deleteLinkById') {
            this.deleteLinkById(msg.data)
        } else if (msg.code === 'deleteClusterById') {
            this.deleteClusterById(msg.data)
            console.log(this.clusters)
        } else if (msg.code === 'updateNode') {
            this.updateNode(msg.data, msg.animated)
        } else if (msg.code === 'updateLink') {
            this.updateLink(msg.data, msg.animated)
        } else if (msg.code === 'moveLink') {
            this.moveLinkBends(msg.data)
        } else if (msg.code === 'removeAllBendMovers') {
            this.removeAllBendMovers()
        } else if (msg.code === 'removeBendMoversFor') {
            this.removeBendMoversForLink(msg.data)
        } else if (msg.code === 'moveCluster') {
            this.moveCluster(msg.data)
        } else if (msg.code === 'removeAllClusterMovers') {
            this.removeAllClusterMovers()
        } else if (msg.code === 'downloadSvg') {
            this.downloadSvg(msg.fileName)
        } else if (msg.code === 'exportSPQR') {
            this.exportSPQRTree(msg.fileName)
        } else if (msg.code === 'test') {
            console.log("test")
        } else {
            console.log("msg cannot be read: " + msg)
        }
    },

    transformCallbackCheck: function () {
        if (this.isTransformCallbackAllowed) {
            this.readjustZoomLevel(
                d3.zoomIdentity.translate(this.model.get('x_pos'), this.model.get('y_pos')).scale(this.model.get('zoom')))
        }
    },

    svgSizeChanged: function () {
        this.width = this.model.get('width')
        this.height = this.model.get('height')

        d3.select(this.svg)
            .attr("width", this.model.get('width'))
            .attr("height", this.model.get('height'))

        if (this.model.get("rescale_on_resize")) this.readjustZoomLevel(this.getInitialTransform(15))
    },

    clickThicknessChanged: function () {
        this.clickThickness = this.model.get("click_thickness")
        let widgetView = this

        d3.select(this.svg).selectAll(".line_click_holder > .line")
            .attr("stroke-width", function (d) {
                return Math.max(d.strokeWidth, widgetView.clickThickness)
            })
    },

    animationDurationChanged: function () {
        this.animationDuration = this.model.get("animation_duration")
    },

    gridSizeChanged: function () {
        this.gridSize = this.model.get('grid_size');
    },

    forceConfigChanged: function () {
        let forceConfig = this.model.get("force_config")

        if (forceConfig.stop || forceConfig.stop == null) {
            this.stopForceLayout()
        } else {
            this.startForceLayout(forceConfig)
        }
    },

    nodeMovementChanged: function () {
        this.isNodeMovementEnabled = this.model.get("node_movement_enabled")

        if (!this.isNodeMovementEnabled) {
            d3.select(this.svg).selectAll(".node").on('mousedown.drag', null)
            d3.select(this.svg).selectAll(".nodeLabel").on('mousedown.drag', null)
        } else {
            d3.select(this.svg).selectAll(".node").call(this.node_drag_handler)
            d3.select(this.svg).selectAll(".nodeLabel").call(this.node_drag_handler)
        }
    },


    startForceLayout: function (forceConfig) {
        let widgetView = this

        this.forceDirected = true
        d3.select(this.svg).selectAll(".node").remove()
        d3.select(this.svg).selectAll("text").remove()
        d3.select(this.svg).selectAll(".line").remove()

        let invisibleNodes = []
        let invisibleLinks = []

        if (widgetView.isClusterGraph) {
            let clusterData = Object.values(this.clusters)
            for (let i = 0; i < clusterData.length; i++) {
                invisibleNodes.push({
                    "id": String(-parseInt(clusterData[i].id) - 1),
                    "name": "test",
                    "x": 0,
                    "y": 0,
                    "shape": 0,
                    "fillColor": {
                        "r": 0,
                        "g": 0,
                        "b": 0,
                        "a": 100
                    },
                    "strokeColor": {
                        "r": 0,
                        "g": 0,
                        "b": 0,
                        "a": 100
                    },
                    "strokeWidth": 1,
                    "nodeWidth": 30,
                    "nodeHeight": 30
                })

                for (let j = 0; j < clusterData[i].nodes.length; j++) {
                    invisibleLinks.push({
                        "strongerLink": true,
                        "id": String((i + 1) * 1000000000 + j),
                        "label": "",
                        "source": String(-parseInt(clusterData[i].id) - 1),
                        "target": clusterData[i].nodes[j],
                        "t_shape": 0,
                        "strokeColor": {
                            "r": 0,
                            "g": 0,
                            "b": 0,
                            "a": 100
                        },
                        "strokeWidth": 1,
                        "sx": 0,
                        "sy": 0,
                        "tx": 0,
                        "ty": 0,
                        "arrow": true,
                        "bends": []
                    })
                }
            }
        }

        let linksData = Object.values(this.links)
        for (let i = 0; i < linksData.length; i++) {
            c.constructForceLink(linksData[i], this.line_holder, this, false)
        }

        let nodesData = Object.values(this.nodes)
        for (let i = 0; i < nodesData.length; i++) {
            c.constructNode(nodesData[i], this.node_holder, this.text_holder, this, false)
        }

        setTimeout(function () {
            widgetView.rescaleAllText()
        }, 10)

        this.simulation = d3.forceSimulation().nodes(nodesData.concat(invisibleNodes))
            .on('end', function () {
                widgetView.syncBackend()
            });

        let link_force = d3.forceLink(linksData.concat(invisibleLinks)).id(function (d) {
            return d.id;
        }).strength(function (link) {
            if (widgetView.isSPQRTree) {
                if (link.virtualLink) {
                    return 0.15
                }
            }

            if (widgetView.isClusterGraph) {
                if (link.strongerLink) {
                    return 0.6;
                } else {
                    if (link.source.clusterId === link.target.clusterId)
                        return 0.2;
                    else
                        return 0.1;
                }
            }

            return 0.2
        })

        let charge_force = d3.forceManyBody().strength(function (d) {
            if (widgetView.isClusterGraph && d.id < 0)
                return forceConfig.chargeForce * 10

            return forceConfig.chargeForce
        });

        let center_force = d3.forceCenter(forceConfig.forceCenterX, forceConfig.forceCenterY);

        this.simulation
            .force("charge_force", charge_force)
            .force("center_force", center_force)
            .force("links", link_force);

        //add tick instructions:
        this.simulation.on("tick", tickActions);

        if (forceConfig.fixStartPosition) {
            d3.select(this.svg).selectAll(".node")
                .attr("x", function (d) {
                    d.fx = d.x
                    d.fy = d.y
                })
        }

        function tickActions() {
            d3.select(widgetView.svg)
                .selectAll(".node")
                .attr("x", function (d) {
                    return d.x - d.nodeWidth / 2;
                })
                .attr("y", function (d) {
                    return d.y - d.nodeHeight / 2;
                })
                .attr("cx", function (d) {
                    return d.x;
                })
                .attr("cy", function (d) {
                    return d.y;
                });

            d3.select(widgetView.svg)
                .selectAll(".nodeLabel")
                .attr("transform", function (d) {
                    return "translate(" + d.x + "," + d.y + ")";
                });

            d3.select(widgetView.svg)
                .selectAll(".line")
                .attr("d", function (d) {
                    d.sx = d.source.x
                    d.sy = d.source.y
                    d.tx = d.target.x
                    d.ty = d.target.y
                    return widgetView.getPathForLine(d.source.x, d.source.y, [], d.target.x, d.target.y, d.t_shape, d.source.id, d.target.id, d);
                });

            d3.select(widgetView.svg)
                .selectAll(".virtualLink")
                .attr("x1", function (d) {
                    let sourceLink = widgetView.links[d.sourceId]
                    return sourceLink.curveX === undefined ? (sourceLink.sx + sourceLink.tx) / 2 : sourceLink.curveX
                })
                .attr("y1", function (d) {
                    let sourceLink = widgetView.links[d.sourceId]
                    return sourceLink.curveY === undefined ? (sourceLink.sy + sourceLink.ty) / 2 : sourceLink.curveY
                })
                .attr("x2", function (d) {
                    let targetLink = widgetView.links[d.targetId]
                    return targetLink.curveX === undefined ? (targetLink.sx + targetLink.tx) / 2 : targetLink.curveX
                })
                .attr("y2", function (d) {
                    let targetLink = widgetView.links[d.targetId]
                    return targetLink.curveY === undefined ? (targetLink.sy + targetLink.ty) / 2 : targetLink.curveY
                })


            if (widgetView.ticksSinceSync % 5 === 0) {
                widgetView.syncBackend()
                widgetView.ticksSinceSync = 0
                if (widgetView.isClusterGraph) {
                    c.constructClusters(widgetView.rootClusterId, widgetView)
                    widgetView.updateClustersInOGDF()
                }
            }
        }
    },

    stopForceLayout: function () {
        if (!this.forceDirected) return

        this.forceDirected = false;
        if (this.simulation != null) {
            this.simulation.stop()
            this.simulation = null
        }

        //reset links to non-force links
        //only needed for SPQR-Trees since other graph types simply get reexported.
        if (this.isSPQRTree) {
            d3.select(this.svg).selectAll(".line").remove()
            let linksData = Object.values(this.links)
            for (let i = 0; i < linksData.length; i++) {
                linksData[i].source = linksData[i].source.id
                linksData[i].target = linksData[i].target.id
                c.constructLink(linksData[i], this.line_holder, this.line_text_holder, this.line_click_holder, this, this.clickThickness, false)
            }
        }
    },

    syncBackend: function () {
        if (!this.isSPQRTree)
            this.send({'code': 'positionUpdate', 'nodes': this.nodes})
    },

    getInitialTransform: function (radius) {
        let nodesData = Object.values(this.nodes)
        let boundingBox = this.getBoundingBox(nodesData, Object.values(this.links))

        let boundingBoxWidth = boundingBox.maxX - boundingBox.minX + radius * 2
        let boundingBoxHeight = boundingBox.maxY - boundingBox.minY + radius * 2

        if (this.isClusterGraph) {
            let rootCluster = this.clusters[this.rootClusterId]
            boundingBoxWidth = Math.max(boundingBoxWidth, rootCluster.x2 - rootCluster.x)
            boundingBoxHeight = Math.max(boundingBoxHeight, rootCluster.y2 - rootCluster.y)
        }

        let scale = Math.min(this.width / boundingBoxWidth, this.height / boundingBoxHeight);
        let x = this.width / 2 - (boundingBox.minX + boundingBoxWidth / 2 - radius) * scale;
        let y = this.height / 2 - (boundingBox.minY + boundingBoxHeight / 2 - radius) * scale;

        if (nodesData.length === 1) {
            scale = 1
            x = this.width / 2 - nodesData[0].x
            y = this.height / 2 - nodesData[0].y
        }

        return d3.zoomIdentity.translate(x, y).scale(scale)
    },

    readjustZoomLevel: function (transform) {
        const widgetView = this
        const svg = d3.select(this.svg)

        //add zoom capabilities
        const zoom = d3.zoom();

        svg.call(zoom.transform, transform)
        svg.call(zoom.on('zoom', zoomed).on('end', zoomEnded));
        svg.call(zoom)

        if (this.g == null)
            return

        this.g.attr("transform", transform)
        this.updateZoomLevelInModel(transform)

        function zoomed({transform}) {
            widgetView.g.attr("transform", transform);
        }

        function zoomEnded({transform}) {
            widgetView.updateZoomLevelInModel(transform)
        }
    },

    updateZoomLevelInModel: function (transform) {
        this.isTransformCallbackAllowed = false
        this.model.set("x_pos", transform.x)
        this.model.set("y_pos", transform.y)
        this.model.set("zoom", transform.k)
        this.model.save_changes()
        this.isTransformCallbackAllowed = true
    },

    downloadSvg: function (fileName) {
        let svgData = this.svg.outerHTML;
        if (!svgData.match(/^<svg[^>]+xmlns="http:\/\/www\.w3\.org\/2000\/svg"/)) {
            svgData = svgData.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
        }
        if (!svgData.match(/^<svg[^>]+"http:\/\/www\.w3\.org\/1999\/xlink"/)) {
            svgData = svgData.replace(/^<svg/, '<svg xmlns:xlink="http://www.w3.org/1999/xlink"');
        }
        const svgBlob = new Blob([svgData], {type: "image/svg+xml;charset=utf-8"});
        const svgUrl = URL.createObjectURL(svgBlob);
        const downloadLink = document.createElement("a");
        downloadLink.href = svgUrl;
        downloadLink.download = fileName + ".svg";
        downloadLink.click();
    },

    exportSPQRTree: function (fileName) {
        const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify({
            'nodes': this.nodes,
            'links': this.links,
            'virtualLinks': this.virtualLinks
        }));
        const downloadAnchorNode = document.createElement('a');
        downloadAnchorNode.setAttribute("href", dataStr);
        downloadAnchorNode.setAttribute("download", fileName + ".json");
        document.body.appendChild(downloadAnchorNode); // required for firefox
        downloadAnchorNode.click();
        downloadAnchorNode.remove();
    },

    moveCluster: function (clusterId) {
        let widgetView = this
        let d = this.clusters[clusterId];

        let clusterData = [{
            "id": d.id,
            "x": (d.x + d.x2) / 2,
            "y": (d.y + d.y2) / 2,
            "strokeWidth": 1
        }]

        let clusterMover = this.clusterMover_holder
            .data(clusterData)
            .enter()
            .append("circle")
            .attr("class", "clusterMover")
            .attr("cx", function (d) {
                return d.x
            })
            .attr("cy", function (d) {
                return d.y
            })
            .attr("id", function (d) {
                return d.id
            })
            .attr("r", 15)
            .attr("fill", "yellow")
            .attr("stroke", "black")
            .attr("stroke-width", function (d) {
                return d.strokeWidth
            })

        const drag_handler_cluster = d3.drag()
            .on("start", dragStarted_cluster)
            .on("drag", dragged_cluster)
            .on("end", dragEnded_cluster);

        clusterMover.call(drag_handler_cluster)

        function dragStarted_cluster(event, d) {
            d3.select(widgetView.svg)
                .selectAll(".clusterMover")
                .filter(function (data) {
                    return data.id === d.id;
                })
                .attr("stroke-width", function (data) {
                    return data.strokeWidth + 1
                });

            d.lastX = event.x
            d.lastY = event.y
        }

        function dragged_cluster(event, d) {
            const clusterId = d.id
            const cluster = widgetView.clusters[clusterId]

            //moving the circle that is dragged
            d3.select(widgetView.svg)
                .selectAll(".clusterMover")
                .filter(function (data) {
                    return data.id === clusterId;
                })
                .attr("cx", event.x)
                .attr("cy", event.y);

            //moving the bounding box of the dragged cluster
            cluster.nodesBoundingBox.minX = cluster.nodesBoundingBox.minX - (d.lastX - event.x)
            cluster.nodesBoundingBox.maxX = cluster.nodesBoundingBox.maxX - (d.lastX - event.x)
            cluster.nodesBoundingBox.minY = cluster.nodesBoundingBox.minY - (d.lastY - event.y)
            cluster.nodesBoundingBox.maxY = cluster.nodesBoundingBox.maxY - (d.lastY - event.y)

            //update all cluster positions
            c.constructClusters(widgetView.rootClusterId, widgetView, false)

            //drag nodes and links
            for (let i = 0; i < cluster.nodes.length; i++) {
                let node = widgetView.nodes[cluster.nodes[i]];
                widgetView.moveNodeAndLinks(node.id, node.x - (d.lastX - event.x), node.y - (d.lastY - event.y), node)
            }

            //update change
            d.lastX = event.x
            d.lastY = event.y
        }

        function dragEnded_cluster(event, d) {
            const cluster = widgetView.clusters[d.id]

            d3.select(widgetView.svg)
                .selectAll(".clusterMover")
                .attr("stroke-width", function (data) {
                    return data.strokeWidth
                });

            //save movers position
            d.x = event.x
            d.y = event.y

            //update OGDF when cluster and nodes got moved.
            widgetView.updateClustersInOGDF()
            for (let i = 0; i < cluster.nodes.length; i++) {
                let node = widgetView.nodes[cluster.nodes[i]];
                widgetView.send({"code": "nodeMoved", "id": node.id, "x": node.x, "y": node.y});
            }
        }
    },

    moveLinkBends: function (d) {
        let widgetView = this
        let bendMoverData = []

        for (let i = 0; i < d.bends.length; i++) {
            bendMoverData.push({
                "id": d.id,
                "x": d.bends[i][0],
                "y": d.bends[i][1],
                "bendIndex": i,
                "strokeWidth": 1
            })
        }

        let bendMovers = this.bendMover_holder
            .data(bendMoverData)
            .enter()
            .append("circle")
            .attr("class", "bendMover")
            .attr("cx", function (d) {
                return d.x
            })
            .attr("cy", function (d) {
                return d.y
            })
            .attr("id", function (d) {
                return d.id
            })
            .attr("r", 7)
            .attr("fill", "yellow")
            .attr("stroke", "black")
            .attr("stroke-width", function (d) {
                return d.strokeWidth
            })

        const drag_handler_bends = d3.drag()
            .on("start", dragStarted_bends)
            .on("drag", dragged_bends)
            .on("end", dragEnded_bends);

        bendMovers.call(drag_handler_bends);

        //Drag functions for bends
        function dragStarted_bends(event, d) {
            d3.select(widgetView.svg)
                .selectAll(".bendMover")
                .filter(function (data) {
                    return data.id === d.id && data.bendIndex === d.bendIndex;
                })
                .attr("stroke-width", function (data) {
                    return data.strokeWidth + 1
                });
        }

        function dragged_bends(event, d) {
            const edgeId = d.id
            const bendIndex = d.bendIndex

            d3.select(widgetView.svg)
                .selectAll(".bendMover")
                .filter(function (data) {
                    return data.id === edgeId && data.bendIndex === bendIndex;
                })
                .attr("cx", event.x)
                .attr("cy", event.y);

            d3.select(widgetView.svg)
                .selectAll(".line")
                .filter(function (data) {
                    return data.id === edgeId;
                })
                .attr("d", function (d) {
                    d.bends[bendIndex][0] = event.x
                    d.bends[bendIndex][1] = event.y
                    return widgetView.getPathForLine(d.sx, d.sy, d.bends, d.tx, d.ty, d.t_shape, d.source, d.target, d);
                })

            if (bendIndex === 0) {
                d3.select(widgetView.svg)
                    .selectAll(".linkLabel")
                    .filter(function (data) {
                        return data.id === edgeId;
                    })
                    .attr("transform", function () { //<-- use transform it's not a g
                        return "translate(" + event.x + "," + event.y + ")";
                    });
            }
        }

        function dragEnded_bends(event, d) {
            d3.select(widgetView.svg)
                .selectAll(".bendMover")
                .attr("stroke-width", function (data) {
                    return data.strokeWidth
                });

            //only send message if bend actually moved
            if (d.x !== event.x || d.y !== event.y) {
                d.x = Math.round(event.x)
                d.y = Math.round(event.y)
                widgetView.send({"code": "bendMoved", "linkId": this.id, "bendIndex": d.bendIndex, "x": d.x, "y": d.y});
            } else {
                //ctrl key not possible because it doesn't activate the drag
                widgetView.send({
                    "code": "bendClicked",
                    "linkId": this.id,
                    "bendIndex": d.bendIndex,
                    "altKey": event.sourceEvent.altKey
                });
            }
        }
    },

    addNode: function (node) {
        if (this.forceDirected) this.stopForceLayout()
        this.nodes[node.id] = node
        c.constructNode(node, this.node_holder, this.text_holder, this, false)

        if (this.isClusterGraph) {
            const cluster = this.clusters[node.clusterId]
            cluster.nodes.push(node.id)
            this.recalculateClusterBoundingBox(cluster)
            c.constructClusters(this.rootClusterId, this, false)
            this.updateClustersInOGDF()
        }

        this.forceConfigChanged()
    },

    addLink: function (link) {
        if (this.forceDirected) this.stopForceLayout()
        this.links[link.id] = link
        c.constructLink(link, this.line_holder, this.line_text_holder, this.line_click_holder, this, this.clickThickness, false)
        this.forceConfigChanged()
    },

    addCluster: function (cluster) {
        this.clusters[cluster.id] = cluster
        //add to parent children
        this.clusters[cluster.parentId].children.push(cluster.id)

        //reassign nodes from other clusters to new cluster
        for (let i = 0; i < cluster.nodes.length; i++) {
            let nodeId = cluster.nodes[i]
            let oldCluster = this.clusters[this.nodes[nodeId].clusterId]
            oldCluster.nodes.splice(oldCluster.nodes.indexOf(nodeId), 1)
            this.nodes[nodeId].clusterId = cluster.id
        }

        c.constructClusters(this.rootClusterId, this)
        this.updateClustersInOGDF()
    },

    deleteNodeById: function (nodeId) {
        if (this.forceDirected) this.stopForceLayout()

        if (this.isClusterGraph) {
            const cluster = this.clusters[this.nodes[nodeId].clusterId]
            cluster.nodes.splice(cluster.nodes.indexOf(nodeId), 1)
            this.recalculateClusterBoundingBox(cluster)
            c.constructClusters(this.rootClusterId, this, false)
            this.updateClustersInOGDF()
        }

        delete this.nodes[nodeId];

        d3.select(this.svg)
            .selectAll(".node")
            .filter(function (d) {
                return d.id === nodeId;
            }).remove()

        d3.select(this.svg)
            .selectAll(".nodeLabel")
            .filter(function (d) {
                return d.id === nodeId;
            }).remove()

        this.forceConfigChanged()
    },

    deleteLinkById: function (linkId) {
        if (this.forceDirected) this.stopForceLayout()
        delete this.links[linkId]

        for (let i = this.virtualLinks.length - 1; i >= 0; i--) {
            if (this.virtualLinks[i].sourceId === linkId || this.virtualLinks[i].targetId === linkId) {
                this.virtualLinks.splice(i, 1);
            }
        }

        this.removeBendMoversForLink(linkId)

        d3.select(this.svg)
            .selectAll(".line")
            .filter(function (d) {
                return d.id === linkId;
            }).remove()

        d3.select(this.svg)
            .selectAll(".linkLabel")
            .filter(function (d) {
                return d.id === linkId;
            }).remove()

        if (this.isSPQRTree) {
            d3.select(widgetView.svg)
                .selectAll(".virtualLink")
                .filter(function (d) {
                    return d.sourceId === movedLinkIds[i] || d.targetId === movedLinkIds[i];
                }).remove()
        }

        this.forceConfigChanged()
    },

    deleteClusterById: function (clusterId) {
        if (this.rootClusterId === clusterId) {
            console.error("You cannot delete the root cluster!")
            return
        }

        let cluster = this.clusters[clusterId]
        let parentCluster = this.clusters[cluster.parentId]

        const index = parentCluster.children.indexOf(clusterId);
        if (index > -1) parentCluster.children.splice(index, 1);

        for (let i = 0; i < cluster.nodes.length; i++) {
            this.nodes[cluster.nodes[i]].clusterId = parentCluster.id
        }

        parentCluster.children = parentCluster.children.concat(cluster.children)
        parentCluster.nodes = parentCluster.nodes.concat(cluster.nodes)

        parentCluster.nodesBoundingBox.minX = Math.min(parentCluster.nodesBoundingBox.minX, cluster.nodesBoundingBox.minX)
        parentCluster.nodesBoundingBox.maxX = Math.max(parentCluster.nodesBoundingBox.maxX, cluster.nodesBoundingBox.maxX)
        parentCluster.nodesBoundingBox.minY = Math.min(parentCluster.nodesBoundingBox.minY, cluster.nodesBoundingBox.minY)
        parentCluster.nodesBoundingBox.maxY = Math.max(parentCluster.nodesBoundingBox.maxY, cluster.nodesBoundingBox.maxY)

        this.calculateClusterSize(this.clusters[cluster.parentId])

        for (let i = 0; i < cluster.children.length; i++) {
            this.clusters[cluster.children[i]].parentId = cluster.parentId
        }

        delete this.clusters[clusterId]

        d3.select(this.svg)
            .selectAll(".cluster")
            .filter(function (d) {
                return d.id === clusterId;
            }).remove()

        //re-rendering clusters without calculating node bounding box
        c.constructClusters(this.rootClusterId, this, false);
        this.updateClustersInOGDF()
    },

    updateNode: function (node, animated) {
        let widgetView = this

        let n = d3.select(this.svg)
            .selectAll(".node")
            .filter(function (d) {
                return d.id === node.id;
            })

        let nl = d3.select(this.svg)
            .selectAll(".nodeLabel")
            .filter(function (d) {
                return d.id === node.id;
            })

        if (widgetView.forceDirected) widgetView.simulation.alphaTarget(0.3).restart()

        n.transition()
            .duration(animated ? this.animationDuration : 1)
            .attr("width", function (d) {
                d.nodeWidth = node.nodeWidth
                return d.nodeWidth
            })
            .attr("height", function (d) {
                d.nodeHeight = node.nodeHeight
                return d.nodeHeight
            })
            .attr("x", function (d) {
                if (widgetView.forceDirected && !widgetView.isNodeMovementEnabled)
                    d.fx = node.x
                else if (widgetView.forceDirected)
                    return

                d.x = node.x
                return d.x - d.nodeWidth / 2
            })
            .attr("y", function (d) {
                if (widgetView.forceDirected && !widgetView.isNodeMovementEnabled)
                    d.fy = node.y
                else if (widgetView.forceDirected)
                    return

                d.y = node.y
                return d.y - d.nodeHeight / 2
            })
            .attr("cx", function (d) {
                if (widgetView.forceDirected && !widgetView.isNodeMovementEnabled)
                    d.fx = node.x
                else if (widgetView.forceDirected)
                    return

                d.x = node.x
                return d.x
            })
            .attr("cy", function (d) {
                if (widgetView.forceDirected && !widgetView.isNodeMovementEnabled)
                    d.fy = node.y
                else if (widgetView.forceDirected)
                    return

                d.y = node.y
                return d.y
            })
            .attr("r", function (d) {
                d.nodeHeight = node.nodeHeight
                return d.nodeHeight / 2
            })
            .attr("fill", function (d) {
                d.fillColor = node.fillColor
                return widgetView.getColorStringFromJson(d.fillColor)
            })
            .attr("stroke", function (d) {
                d.strokeColor = node.strokeColor
                return widgetView.getColorStringFromJson(d.strokeColor)
            })
            .attr("stroke-width", function (d) {
                d.strokeWidth = node.strokeWidth
                return d.strokeWidth
            })

        if (this.isClusterGraph) {
            //todo check if cluster of node changed

            const cluster = this.clusters[node.clusterId]
            //todo method that takes cluster and node to recalc
            this.recalculateClusterBoundingBox(cluster)
            c.constructClusters(this.rootClusterId, this, false)
            this.updateClustersInOGDF()
        }

        if (widgetView.forceDirected) {
            setTimeout(function () {
                widgetView.simulation.alphaTarget(0)
            }, 1000)
        }

        let textChanged = true
        nl.text(function (d) {
            if (d.name !== node.name) {
                d.name = node.name
                d.labelWidth = 0
            } else {
                textChanged = false
            }
            return d.name;
        }).style("font-size", function (d) {
            if (textChanged)
                return 1 + 'em'

            return d.fontSize + 'em'
        })

        if (textChanged) {
            setTimeout(function () {
                widgetView.rescaleTextById(node.id)
            }, 10)
        }

        nl.transition()
            .duration(animated ? this.animationDuration : 1)
            .attr("transform", function (d) { //<-- use transform it's not a g
                if (widgetView.forceDirected && widgetView.isNodeMovementEnabled)
                    return

                d.x = node.x
                d.y = node.y
                return "translate(" + d.x + "," + d.y + ")";
            })
    },

    addBendsToLink: function (link, totalBendAmount) {
        let points = [[link.sx, link.sy]].concat(link.bends).concat([[link.tx, link.ty]])

        while (totalBendAmount > points.length - 2) {
            for (let i = points.length - 2; i >= 0 && totalBendAmount > points.length - 2; i--) {
                let newPoint = [(points[i][0] + points[i + 1][0]) / 2, (points[i][1] + points[i + 1][1]) / 2]
                points.splice(i + 1, 0, newPoint);
            }
        }

        points.shift()
        points.pop()

        link.bends = points

        return link
    },

    updateLink: function (link, animated) {
        let bendMoverActive = false
        d3.select(this.svg)
            .selectAll(".bendMover")
            .filter(function (d) {
                if (d.id === link.id) bendMoverActive = true
                return d.id === link.id;
            }).remove()

        if (bendMoverActive)
            this.moveLinkBends(link)

        if (!animated) {
            this.deleteLinkById(link.id)
            this.addLink(link)
            return
        }

        //artificially add bends to make animation better
        let currentLink = this.links[link.id]
        let paddedLink = null

        if (currentLink !== null && currentLink.bends.length !== link.bends.length) {
            if (currentLink.bends.length < link.bends.length) {
                this.deleteLinkById(link.id)
                this.addLink(this.addBendsToLink(JSON.parse(JSON.stringify(currentLink)), link.bends.length))
            } else {
                paddedLink = this.addBendsToLink(JSON.parse(JSON.stringify(link)), currentLink.bends.length)
            }
        }

        let widgetView = this
        let l = d3.select(this.svg)
            .selectAll(".line_holder > .line")
            .filter(function (d) {
                return d.id === link.id;
            })

        let lc = d3.select(this.svg)
            .selectAll(".line_click_holder > .line")
            .filter(function (d) {
                return d.id === link.id;
            })

        let ll = d3.select(this.svg)
            .selectAll(".linkLabel")
            .filter(function (d) {
                return d.id === link.id;
            })

        l.transition()
            .duration(this.animationDuration)
            .attr("d", function (d) {
                let newLink = paddedLink == null ? link : paddedLink
                d.source = newLink.source
                d.target = newLink.target
                d.sx = newLink.sx
                d.sy = newLink.sy
                d.bends = newLink.bends
                d.tx = newLink.tx
                d.ty = newLink.ty

                return widgetView.getPathForLine(d.sx, d.sy, d.bends, d.tx, d.ty, d.t_shape, d.source, d.target, d);
            })
            .attr("stroke", function (d) {
                d.strokeColor = link.strokeColor
                return widgetView.getColorStringFromJson(d.strokeColor)
            })
            .attr("stroke-width", function (d) {
                d.strokeWidth = link.strokeWidth
                return d.strokeWidth
            })

        lc.transition()
            .duration(this.animationDuration)
            .attr("d", function (d) {
                d.source = link.source
                d.target = link.target
                d.sx = link.sx
                d.sy = link.sy
                d.bends = link.bends
                d.tx = link.tx
                d.ty = link.ty

                return widgetView.getPathForLine(d.sx, d.sy, d.bends, d.tx, d.ty, d.t_shape, d.source, d.target, d);
            })
            .attr("stroke-width", function (d) {
                d.strokeWidth = link.strokeWidth
                return Math.max(d.strokeWidth, widgetView.clickThickness)
            })

        ll.transition()
            .duration(this.animationDuration)
            .text(function (d) {
                d.label = link.label
                return d.label;
            })
            .attr("transform", function (d) { //<-- use transform it's not a g
                d.label_x = link.label_x
                d.label_y = link.label_y
                return "translate(" + d.label_x + "," + d.label_y + ")";
            })

        if (paddedLink != null) {
            setTimeout(() => {
                this.deleteLinkById(link.id)
                this.addLink(link)
            }, this.animationDuration);
        }
    },

    updateCluster: function (clusterData, animated) {
        let widgetView = this

        let c = d3.select(this.svg)
            .selectAll(".cluster")
            .filter(function (d) {
                return d.id === clusterData.id;
            })

        if (c == null) {
            console.error("ClusterId: " + clusterData.id + " could not be found.")
            return
        }

        const line = d3.line()

        c.transition()
            .duration(animated ? this.animationDuration : 1)
            .attr("d", function (d) {
                let points = [[d.x, d.y], [d.x2, d.y], [d.x2, d.y2], [d.x, d.y2], [d.x, d.y]]
                return line(points)
            })
            .attr("stroke", function (d) {
                return widgetView.getColorStringFromJson(d.strokeColor)
            })
            .attr("stroke-width", function (d) {
                return d.strokeWidth
            })
            .attr("fill", "none")
    },

    clearGraph: function () {
        this.nodes = {}
        this.links = {}
        this.clusters = {}
        this.virtualLinks = []

        d3.select(this.svg).selectAll(".node").remove()
        d3.select(this.svg).selectAll("text").remove()
        d3.select(this.svg).selectAll(".line").remove()
        d3.select(this.svg).selectAll(".linkLabel").remove()
        d3.select(this.svg).selectAll(".virtualLink").remove()
        d3.select(this.svg).selectAll(".cluster").remove()
    },

    getBoundingBox: function (nodes, links) {
        let boundingBox = {
            "minX": Number.MAX_VALUE,
            "maxX": Number.MIN_VALUE,
            "minY": Number.MAX_VALUE,
            "maxY": Number.MIN_VALUE,
        }

        for (let i = 0; i < nodes.length; i++) {
            if (nodes[i].x < boundingBox.minX) boundingBox.minX = nodes[i].x
            if (nodes[i].x > boundingBox.maxX) boundingBox.maxX = nodes[i].x

            if (nodes[i].y < boundingBox.minY) boundingBox.minY = nodes[i].y
            if (nodes[i].y > boundingBox.maxY) boundingBox.maxY = nodes[i].y
        }

        if (links != null) {
            for (let i = 0; i < links.length; i++) {
                for (let j = 0; j < links[i].bends.length; j++) {
                    let bend = links[i].bends[j]

                    if (bend[0] < boundingBox.minX) boundingBox.minX = bend[0]
                    if (bend[0] > boundingBox.maxX) boundingBox.maxX = bend[0]

                    if (bend[1] < boundingBox.minY) boundingBox.minY = bend[1]
                    if (bend[1] > boundingBox.maxY) boundingBox.maxY = bend[1]
                }
            }
        }

        return boundingBox
    },

    removeAllBendMovers: function () {
        d3.select(this.svg).selectAll(".bendMover").remove()
    },

    removeAllClusterMovers: function () {
        d3.select(this.svg).selectAll(".clusterMover").remove()
    },

    moveNodeAndLinks: function (nodeId, newX, newY, d) {
        let widgetView = this

        //move node
        d3.select(widgetView.svg)
            .selectAll(".node")
            .filter(function (data) {
                return data.id === nodeId;
            })
            .attr("cx", function (d) {
                d.x = newX
                return newX
            })
            .attr("cy", function (d) {
                d.y = newY
                return newY
            })
            .attr("x", newX - d.nodeWidth / 2)
            .attr("y", newY - d.nodeHeight / 2);

        //move node-label
        d3.select(widgetView.svg)
            .selectAll(".nodeLabel")
            .filter(function (data) {
                return data.id === nodeId;
            })
            .attr("transform", function () { //<-- use transform it's not a g
                return "translate(" + newX + "," + newY + ")";
            });

        let labelsToMoveIds = []
        let movedLinkIds = []
        //move attached links
        d3.select(widgetView.svg)
            .selectAll(".line")
            .filter(function (data) {
                return data.source === nodeId || data.target === nodeId;
            })
            .attr("d", function (d) {
                movedLinkIds.push(d.id)

                if (d.source === nodeId) {
                    d.sx = newX
                    d.sy = newY
                }
                if (d.target === nodeId) {
                    d.tx = newX
                    d.ty = newY
                }

                if (d.bends.length === 0) {
                    labelsToMoveIds.push(d.id)
                }

                return widgetView.getPathForLine(d.sx, d.sy, d.bends, d.tx, d.ty, d.t_shape, d.source, d.target, d);
            })

        //move link-label
        for (let i = 0; i < labelsToMoveIds.length; i++) {
            d3.select(widgetView.svg)
                .selectAll(".linkLabel")
                .filter(function (data) {
                    return data.id === labelsToMoveIds[i];
                })
                .attr("transform", function (data) { //<-- use transform it's not a g
                    let labelX = (data.sx + data.tx) / 2
                    let labelY = (data.sy + data.ty) / 2
                    return "translate(" + labelX + "," + labelY + ")";
                });
        }

        //move VirtualLink
        if (widgetView.isSPQRTree && movedLinkIds.length !== 0) {
            for (let i = 0; i < movedLinkIds.length; i++) {
                d3.select(widgetView.svg)
                    .selectAll(".virtualLink")
                    .filter(function (d) {
                        return d.sourceId === movedLinkIds[i] || d.targetId === movedLinkIds[i];
                    })
                    .attr("x1", function (d) {
                        let sourceLink = widgetView.links[d.sourceId]
                        return sourceLink.curveX === undefined ? (sourceLink.sx + sourceLink.tx) / 2 : sourceLink.curveX
                    })
                    .attr("y1", function (d) {
                        let sourceLink = widgetView.links[d.sourceId]
                        return sourceLink.curveY === undefined ? (sourceLink.sy + sourceLink.ty) / 2 : sourceLink.curveY
                    })
                    .attr("x2", function (d) {
                        let targetLink = widgetView.links[d.targetId]
                        return targetLink.curveX === undefined ? (targetLink.sx + targetLink.tx) / 2 : targetLink.curveX
                    })
                    .attr("y2", function (d) {
                        let targetLink = widgetView.links[d.targetId]
                        return targetLink.curveY === undefined ? (targetLink.sy + targetLink.ty) / 2 : targetLink.curveY
                    })
            }
        }
    },

    removeBendMoversForLink: function (linkId) {
        d3.select(this.svg)
            .selectAll(".bendMover")
            .filter(function (d) {
                return d.id === linkId;
            }).remove()
    },

    // Defines how the widget gets rendered into the DOM
    render: function () {
        //todo check for empty nodes obj
        if (this.links.length === 0 && this.nodes.length === 0)
            return

        if (this.el.childNodes.length === 0) {
            let svgId = "G" + Math.random().toString(16).slice(2)

            this.svg = document.createElementNS("http://www.w3.org/2000/svg", "svg")
            this.svg.setAttribute("id", svgId)
            this.svg.setAttribute("width", this.width);
            this.svg.setAttribute("height", this.height);

            this.el.appendChild(this.svg)
        }

        this.draw_graph()

        let widgetView = this;

        setTimeout(function () {
            widgetView.rescaleAllText()
        }, 10)
    },

    updateClustersInOGDF: function () {
        let clustersData = Object.values(this.clusters)
        for (let i = 0; i < clustersData.length; i++) {
            let c = clustersData[i]
            this.send({
                'code': 'updateClusterPosition',
                'id': c.id,
                'x': c.x,
                'y': c.y,
                'width': c.x2 - c.x,
                'height': c.y2 - c.y,
            });
        }
    },

    recalculateClusterBoundingBox: function (cluster) {
        let nodes = []
        for (let i = 0; i < cluster.nodes.length; i++) {
            nodes.push(this.nodes[cluster.nodes[i]])
        }

        cluster.nodesBoundingBox = this.getBoundingBox(nodes)
    },

    calculateClusterSize: function (cluster) {
        //todo create bounding box for each node in preparation for shapes
        //nodeOffset in this case will be nodeWidth/Height
        let nodeOffset = 10
        let clusterOffset = 5

        cluster.x = cluster.nodesBoundingBox.minX - nodeOffset
        cluster.y = cluster.nodesBoundingBox.minY - nodeOffset
        cluster.x2 = cluster.nodesBoundingBox.maxX + nodeOffset
        cluster.y2 = cluster.nodesBoundingBox.maxY + nodeOffset

        for (let i = 0; i < cluster.children.length; i++) {
            cluster.x = Math.min(cluster.x, this.clusters[cluster.children[i]].x)
            cluster.y = Math.min(cluster.y, this.clusters[cluster.children[i]].y)
            cluster.x2 = Math.max(cluster.x2, this.clusters[cluster.children[i]].x2)
            cluster.y2 = Math.max(cluster.y2, this.clusters[cluster.children[i]].y2)
        }

        cluster.x = cluster.x - clusterOffset
        cluster.y = cluster.y - clusterOffset
        cluster.x2 = cluster.x2 + clusterOffset
        cluster.y2 = cluster.y2 + clusterOffset
    },

    constructCluster: function (clusterData, cluster_holder, widgetView) {
        const line = d3.line()

        cluster_holder
            .data([clusterData])
            .enter()
            .append("path")
            .attr("class", "cluster")
            .attr("id", function (d) {
                return d.id
            })
            .attr("d", function (d) {
                let points = [[d.x, d.y], [d.x2, d.y], [d.x2, d.y2], [d.x, d.y2], [d.x, d.y]]
                return line(points)
            })
            .attr("stroke", function (d) {
                return widgetView.getColorStringFromJson(d.strokeColor)
            })
            .attr("stroke-width", function (d) {
                return d.strokeWidth
            })
            .attr("fill", "none")
            .on("click", function (event, d) {
                widgetView.send({
                    "code": "clusterClicked",
                    "id": d.id,
                    "altKey": event.altKey,
                    "ctrlKey": event.ctrlKey
                });

            })
    },

    getColorStringFromJson(color) {
        return "rgba(" + color.r + ", " + color.g + ", " + color.b + ", " + color.a + ")"
    },

    getSelfLoopPath: function (x1, y1, x2, y2) {
        let xRotation = -45;
        let largeArc = 1;
        let drx = 30;
        let dry = 20;
        return "M" + x1 + "," + y1 + "A" + drx + "," + dry + " " + xRotation + "," + largeArc + "," + 1 + " " + (x2 + 1) + "," + (y2 + 1);
    },

    draw_graph() {
        let widgetView = this
        const svg = d3.select(this.svg)

        svg.on("click", function (event) {
            let backgroundClicked
            if (event.path === undefined) {
                backgroundClicked = event.originalTarget.nodeName === "svg"
            } else {
                backgroundClicked = event.path[0].nodeName === "svg"
            }

            widgetView.send({
                "code": "svgClicked",
                "x": event.offsetX,
                "y": event.offsetY,
                "altKey": event.altKey,
                "ctrlKey": event.ctrlKey,
                "backgroundClicked": backgroundClicked
            });
        })

        let nodesData = Object.values(this.nodes)
        let linksData = Object.values(this.links)

        let radius = nodesData.length > 0 ? nodesData[0].nodeWidth / 2 : 0

        d3.select(this.svg).selectAll(".everything").remove()
        //add encompassing group for the zoom
        this.g = svg.append("g").attr("class", "everything");

        constructArrowElements(radius)

        //clusters
        this.cluster_holder = this.g.append("g")
            .attr("class", "cluster_holder")
            .selectAll(".cluster")

        if (this.clusters != null && this.isClusterGraph)
            c.constructClusters(this.rootClusterId, this)

        this.updateClustersInOGDF()

        //links
        this.line_holder = this.g.append("g")
            .attr("class", "line_holder")
            .selectAll(".line")

        this.line_click_holder = this.g.append("g")
            .attr("class", "line_click_holder")
            .selectAll(".line")

        this.line_text_holder = this.g.append("g")
            .attr("class", "line_text_holder")
            .selectAll(".lineText")

        for (let i = 0; i < linksData.length; i++) {
            if (widgetView.isSPQRTree && linksData[i].virtualLink) continue
            c.constructLink(linksData[i], this.line_holder, this.line_text_holder, this.line_click_holder, widgetView, this.clickThickness, false)
        }

        this.bendMover_holder = this.g.append("g").attr("class", "bendMover_holder").selectAll("bendMover")

        //SPQR

        this.virtual_line_holder = this.g.append("g")
            .attr("class", "virtual_line_holder")
            .selectAll(".virtualLink")

        for (let i = 0; i < this.virtualLinks.length; i++) {
            c.constructVirtualLink(this.virtualLinks[i], this.virtual_line_holder, widgetView)
        }

        //nodes
        widgetView.node_drag_handler = d3.drag()
            .on("start", dragStarted_nodes)
            .on("drag", dragged_nodes)
            .on("end", dragEnded_nodes);

        this.node_holder = this.g.append("g")
            .attr("class", "node_holder")
            .selectAll(".node")

        this.text_holder = this.g.append("g")
            .attr("class", "text_holder")
            .selectAll(".nodeLabel")

        for (let i = 0; i < nodesData.length; i++) {
            c.constructNode(nodesData[i], this.node_holder, this.text_holder, widgetView, false)
        }

        this.clusterMover_holder = this.g.append("g").attr("class", "clusterMover_holder").selectAll("clusterMover")

        function constructArrowElements(radius) {
            //construct arrow for circle
            svg.append("svg:defs").selectAll("marker")
                .data(["endCircle"])
                .enter().append("svg:marker")
                .attr("id", String)
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", radius * 4 / 3 + 8)
                .attr("refY", 0)
                .attr("markerWidth", 8)
                .attr("markerHeight", 8)
                .attr("orient", "auto")
                .attr("fill", "black")
                .append("svg:path")
                .attr("d", "M0,-5L10,0L0,5");

            //construct arrow for square
            svg.append("svg:defs").selectAll("marker")//
                .data(["endSquare"])      // Different link/path types can be defined here
                .enter().append("svg:marker")    // This section adds in the arrows
                .attr("id", String)
                .attr("viewBox", "0 -5 10 10")
                .attr("refX", 10)
                .attr("refY", 0)
                .attr("markerWidth", 5)
                .attr("markerHeight", 5)
                .attr("orient", "auto")
                .attr("stroke", "#000")
                .attr("fill", "#000")
                .append("svg:path")
                .attr("d", "M0,-5L10,0L0,5")
                .style("stroke-width", "0.3px")
        }

        this.readjustZoomLevel(this.getInitialTransform(radius))

        //Drag functions for nodes
        function dragStarted_nodes(event, d) {
            const nodeId = this.id

            d.startX = d.x
            d.startY = d.y

            //makes stroke bigger for dragged node
            d3.select(widgetView.svg)
                .selectAll(".node")
                .filter(function (data) {
                    return data.id === nodeId;
                })
                .attr("stroke-width", function (data) {
                    return data.strokeWidth + 1
                });

            if (widgetView.forceDirected && !event.active) widgetView.simulation.alphaTarget(0.3).restart();

            if (widgetView.isClusterGraph) {
                //calculate nodeBoundingBox without dragged node
                let cluster = widgetView.clusters[d.clusterId]
                let nodes = []
                for (let i = 0; i < cluster.nodes.length; i++) {
                    if (cluster.nodes[i] !== nodeId)
                        nodes.push(widgetView.nodes[cluster.nodes[i]])
                }

                //todo test if BB causes problems when nodes is empty
                cluster.bbWoutDragged = widgetView.getBoundingBox(nodes)
            }
        }

        function dragged_nodes(event, d) {
            let newX = event.x;
            let newY = event.y;

            //grid snapping
            if (widgetView.gridSize !== 0) {
                newX = widgetView.gridSize * Math.floor((event.x / widgetView.gridSize) + 0.5);
                newY = widgetView.gridSize * Math.floor((event.y / widgetView.gridSize) + 0.5);
            }

            //force layout
            if (widgetView.forceDirected) {
                event.subject.fx = newX;
                event.subject.fy = newY;
                return
            }

            const nodeId = this.id
            const line = d3.line()

            widgetView.moveNodeAndLinks(nodeId, newX, newY, d)

            //move clusters
            if (widgetView.isClusterGraph) {
                let cluster = widgetView.clusters[d.clusterId]
                cluster.nodesBoundingBox.minX = Math.min(cluster.bbWoutDragged.minX, event.x)
                cluster.nodesBoundingBox.minY = Math.min(cluster.bbWoutDragged.minY, event.y)
                cluster.nodesBoundingBox.maxX = Math.max(cluster.bbWoutDragged.maxX, event.x)
                cluster.nodesBoundingBox.maxY = Math.max(cluster.bbWoutDragged.maxY, event.y)

                for (let c = cluster; c !== null; c = widgetView.clusters[c.parentId]) {
                    widgetView.calculateClusterSize(c)

                    d3.select(widgetView.svg)
                        .selectAll(".cluster")
                        .filter(function (data) {
                            return data.id === c.id
                        })
                        .attr("d", function (d) {
                            let points = [[d.x, d.y], [d.x2, d.y], [d.x2, d.y2], [d.x, d.y2], [d.x, d.y]]
                            return line(points)
                        })

                    if (c.parentId === null)
                        break;
                }
            }
        }

        function dragEnded_nodes(event, d) {
            const nodeId = this.id

            //returns stroke to normal for dragged node
            d3.select(widgetView.svg)
                .selectAll(".node")
                .filter(function (data) {
                    return data.id === nodeId;
                })
                .attr("stroke-width", function (data) {
                    return data.strokeWidth
                });

            if (widgetView.forceDirected && !event.active) widgetView.simulation.alphaTarget(0);

            //if node only got clicked and not moved
            if (d.startX === event.x && d.startY === event.y) {
                if (widgetView.forceDirected) {
                    event.subject.fx = null;
                    event.subject.fy = null;
                }

                widgetView.send({
                    "code": "nodeClicked",
                    "id": nodeId,
                    "altKey": event.sourceEvent.altKey,
                    "ctrlKey": event.sourceEvent.ctrlKey
                });
            } else {
                d.x = Math.round(event.x)
                d.y = Math.round(event.y)

                if (widgetView.gridSize !== 0) {
                    d.x = widgetView.gridSize * Math.floor((event.x / widgetView.gridSize) + 0.5);
                    d.y = widgetView.gridSize * Math.floor((event.y / widgetView.gridSize) + 0.5);
                }
                if (!widgetView.isSPQRTree)
                    widgetView.send({"code": "nodeMoved", "id": this.id, "x": d.x, "y": d.y});
                widgetView.updateClustersInOGDF();
            }

            if (widgetView.isClusterGraph) delete widgetView.clusters[d.clusterId].bbWoutDragged
        }
    },

    rescaleAllText() {
        d3.select(this.svg).selectAll(".nodeLabel").style("font-size", this.adaptLabelFontSize)
    },

    rescaleTextById(nodeId) {
        d3.select(this.svg).selectAll(".nodeLabel").filter(function (d) {
            return d.id === nodeId;
        }).style("font-size", this.adaptLabelFontSize)
    },

    adaptLabelFontSize(d) {
        let labelAvailableWidth = d.nodeWidth - 2;

        if (typeof d.labelWidth === 'undefined' || d.labelWidth === 0)
            d.labelWidth = this.getComputedTextLength();

        // There is enough space for the label so leave it as is.
        if (d.labelWidth <= labelAvailableWidth) {
            d.fontSize = 1
            return '1em';
        } else {
            d.fontSize = (labelAvailableWidth / d.labelWidth - 0.01)
            return d.fontSize + 'em';
        }
    },

    getPathForLine(sx, sy, bends, tx, ty, shape, sId, tId, link) {
        //self loop
        if (sId === tId && bends.length === 0) {
            return this.getSelfLoopPath(sx, sy, tx, ty)
        }

        let M = 20

        //spread out parallel edges of P-nodes
        if (this.isSPQRTree && link.isPnode && link.isVlinkAttached) {
            let linkToLookAt
            for (let i = 0; i < this.virtualLinks.length; i++) {
                if (this.virtualLinks[i].sourceId === link.id)
                    linkToLookAt = this.links[this.virtualLinks[i].targetId]

                if (this.virtualLinks[i].targetId === link.id)
                    linkToLookAt = this.links[this.virtualLinks[i].sourceId]
            }

            let middleOfOtherX = (linkToLookAt.sx + linkToLookAt.tx) / 2
            let myMiddleX = (sx + tx) / 2

            if (middleOfOtherX < myMiddleX)
                M = M * -1

            return this.draw_curve(sx, sy, tx, ty, M, link)
        }

        const line = d3.line()
        let points = [[sx, sy]].concat(bends)

        //shape is a rectangle
        if (shape === 0) {
            let sourceX = sx
            let sourceY = sy

            if (bends.length !== 0) {
                sourceX = bends[bends.length - 1][0]
                sourceY = bends[bends.length - 1][1]
            }

            let node = this.nodes[tId]

            let inter = this.pointOnRect(sourceX, sourceY,
                tx - node.nodeWidth / 2, ty - node.nodeHeight / 2,
                tx + node.nodeWidth / 2, ty + node.nodeHeight / 2, false);

            return line(points) + "L" + inter.x + "," + inter.y;
        }

        points = points.concat([[tx, ty]])
        return line(points)
    },

    draw_curve(sx, sy, tx, ty, scale, link) {
        //get point in the middle
        let middleX = (tx + sx) / 2
        let middleY = (ty + sy) / 2

        //make sure that the orientation is correct.
        let xDiff = tx - sx
        let yDiff = ty - sy
        let theta = Math.atan(yDiff / (xDiff + 0.1))
        let aSign = (xDiff < 0 ? -1 : 1)

        //find offsets
        let offsetX = scale * aSign * Math.sin(theta)
        let offsetY = scale * aSign * Math.cos(theta)

        //calculate control point used for path
        let controlPointX = middleX - offsetX
        let controlPointY = middleY + offsetY

        //save point where middle of path will actually be drawn
        link.curveX = middleX - offsetX * 0.5
        link.curveY = middleY + offsetY * 0.5

        return "M" + sx + "," + sy +
            "Q" + controlPointX + "," + controlPointY +
            " " + tx + "," + ty
    },

    /**
     * Finds the intersection point between
     *     * the rectangle
     *       with parallel sides to the x and y axes
     *     * the half-line pointing towards (x,y)
     *       originating from the middle of the rectangle
     *
     * Note: the function works given min[XY] <= max[XY],
     *       even though minY may not be the "top" of the rectangle
     *       because the coordinate system is flipped.
     *
     * @param x:Number x-coord of point to build the line segment from
     * @param y:Number y-coord of point to build the line segment from
     * @param minX:Number the "left" side of the rectangle
     * @param minY:Number the "top" side of the rectangle
     * @param maxX:Number the "right" side of the rectangle
     * @param maxY:Number the "bottom" side of the rectangle
     * @param check:boolean (optional) whether to treat point inside the rect as error
     * @return an object with x and y members for the intersection
     * @throws if check == true and (x,y) is inside the rectangle
     * @author TWiStErRob
     * @see <a href="https://stackoverflow.com/a/31254199/253468">source</a>
     * @see <a href="https://stackoverflow.com/a/18292964/253468">based on</a>
     */
    pointOnRect(x, y, minX, minY, maxX, maxY, check) {
        //assert minX <= maxX;
        //assert minY <= maxY;
        check = true
        //todo change check
        if (check && (minX <= x && x <= maxX) && (minY <= y && y <= maxY)) {
            console.log("Point " + [x, y] + "cannot be inside " + "the rectangle: " + [minX, minY] + " - " + [maxX, maxY] + ".");
            return {
                x: (minX + maxX) / 2,
                y: (minY + maxY) / 2
            };
        }
        const midX = (minX + maxX) / 2;
        const midY = (minY + maxY) / 2;
        // if (midX - x == 0) -> m == ±Inf -> minYx/maxYx == x (because value / ±Inf = ±0)
        const m = (midY - y) / (midX - x);

        if (x <= midX) { // check "left" side
            const minXy = m * (minX - x) + y;
            if (minY <= minXy && minXy <= maxY)
                return {
                    x: minX,
                    y: minXy
                };
        }

        if (x >= midX) { // check "right" side
            const maxXy = m * (maxX - x) + y;
            if (minY <= maxXy && maxXy <= maxY)
                return {
                    x: maxX,
                    y: maxXy
                };
        }

        if (y <= midY) { // check "top" side
            const minYx = (minY - y) / m + x;
            if (minX <= minYx && minYx <= maxX)
                return {
                    x: minYx,
                    y: minY
                };
        }

        if (y >= midY) { // check "bottom" side
            const maxYx = (maxY - y) / m + x;
            if (minX <= maxYx && maxYx <= maxX)
                return {
                    x: maxYx,
                    y: maxY
                };
        }

        // Should never happen :) If it does, please tell me!
        throw "Cannot find intersection for " + [x, y] + " inside rectangle " + [minX, minY] + " - " + [maxX, maxY] + ".";
    },
});

module.exports = {
    WidgetModel: WidgetModel,
    WidgetView: WidgetView,
};