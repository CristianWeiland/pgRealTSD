<template>
    <div v-if="availableAttributes && availableAttributes.length">
        <div v-for="i in nGraphs" :key="i">
            <div :class="[`col-xs-${12/nGraphs}`]">
                <div v-for="(attrObj, index) in availableAttributes" :key="index" style="background-color: #fff">
                    <graph
                        v-if="index % nGraphs == i-1 && server && attrObj && attrObj.attribute"
                        :serverName="server.name"
                        :attr="attrObj.attribute"
                        :hrAttr="humanReadableAttr(attrObj.attribute)"
                        :configurations="configurations">
                    </graph>
                </div>  
            </div>
        </div>
    </div>
    <div style="height: 100px; font-size: 30px; margin-top: 50px;" v-else-if="availableAttributes">
        This server has no available data types.
    </div>
</template>

<script>
import Graph from './Graph';

export default {
    name: 'graphs',
    props: {
        server: {
            type: Object,
            required: true,
        },
        configurations: {
            type: Object,
            required: true,
        },
    },
    components: {
        Graph,
    },
    computed: {
        nGraphs() {
            try {
                return parseInt(this.configurations.graphsPerLine, 10);
            } catch (e) {
                return 2;
            }
        },
        availableAttributes() {
            try {
                return this.server.data_list;
            } catch (e) {
                return null;
            }
        },
    },
    methods: {
        humanReadableAttr(attr) {
            const parser = {
                r: 'Waiting processes',
                b: 'Sleeping processes',
                swpd: 'Virtual memory',
                free: 'Idle memory',
                buff: 'Memory used as buffers',
                cache: 'Memory used as cache',
                inact: 'Inactive memory',
                active: 'Active memory',
                si: 'Memory swapped in',
                so: 'Memory swapped out',
                bi: 'IO (in)',
                bo: 'IO (out)',
                in: 'System interrupts per second',
                cs: 'Context switches per second',
                us: 'CPU User time',
                sy: 'CPU System time',
                id: 'CPU Idle time',
                wa: 'CPU IO wait time',
                st: 'CPU Stolen from a virtual machine tim',
                requests: 'Number of requests',
                responses: 'Number of responses',
                states: 'States',
            };
            return parser[attr];
        },
    },
};
</script>
