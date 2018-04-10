<template>
    <div class="box">
        <span
            style="float: right; margin-top: 20px"
            @click="expanded = !expanded"
            class="expand-icon glyphicon glyphicon-plus"
            :class="{ 'glyphicon-plus': !expanded, 'glyphicon-minus': expanded }"></span>
        <h2 style="padding-right: 60px">{{hrAttr}} ({{utils.capitalize(attr)}})</h2>
        <transition name="slide-fade"
            @before-enter="beforeEnter" @enter="enter"
            @before-leave="beforeLeave" @leave="leave">
            <div class="animation" v-show="expanded">
                <div :id="`chart-${attr}`" class="limit-width"></div>
            </div>
        </transition>
    </div>
</template>

<script>
import { getServerAttrPer } from '../services/server';
import utils from '../utils/utils';


export default {
    name: 'graphs',
    props: {
        serverName: {
            type: String,
            required: true,
        },
        attr: {
            type: String,
            required: true,
        },
        hrAttr: {
            type: String,
            required: true,
        },
        configurations: {
            type: Object,
            required: true,
        },
    },
    data() {
        if (this.configurations.initializeExpanded) {
            this.expandBox();
        }
        return {
            expanded: this.configurations.initializeExpanded || false,
            intervalId: null,
            hasData: false,
            chart: null,
            utils,
            dataArr: [0, 1],
            /* fake data to test */
            fakeVal: 2,
            fakeInstant: 1,
        };
    },
    mounted() {
        this.createChart();
    },
    computed: {
        interval() {
            return this.configurations.interval || 10;
        },
        period() {
            return this.configurations.period || 5;
        },
        spacing() {
            return this.configurations.spacing || 3;
        },
        chartData() {
            return this.dataArr;
        },
    },
    methods: {
        beforeEnter: function(el) {
          el.style.height = '0';
        },
        enter: function(el) {
          el.style.height = el.scrollHeight + 'px';
        },
        beforeLeave: function(el) {
          el.style.height = el.scrollHeight + 'px';
        },
        leave: function(el) {
          el.style.height = '0';
        },
        updateData() {
            // TODO: Get data from API
            this.fakeVal += 2;
            this.fakeInstant += 1;
            const shift = this.chart.series[0].data.length >= this.configurations.maxPoints;
            this.chart.series[0].addPoint([this.fakeVal, this.fakeInstant], true, shift);
        },
        createChart() {
            let vm = this;
            let chartOptions = {
                chart: {
                    borderWidth: 0,
                    type: 'spline',
                    animation: this.Highcharts.svg, // don't animate in old IE
                    marginRight: 10,
                },
                credits: false,
                title: {
                    text: null,
                },
                xAxis: {
                    title: {
                        text: 'Time'
                    },
                    type: 'datetime',
                    tickPixelInterval: 30,
                },
                yAxis: {
                    title: {
                        text: utils.capitalize(this.attr),
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }],
                },
                tooltip: {
                    formatter: function() {
                        /* TODO: Parse time
                        return '<b>' + this.attr + '</b><br/>Time: ' +
                            this.Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +
                            '<br/>Value: ' + this.y;
                        */
                        return `Attr: <b>${vm.attr}</b><br/>Time: ${this.x}<br/>Value: ${this.y}`;
                    },
                },
                series: [{
                    name: 'Memória (KBs)', // TODO
                    data: this.chartData,
                }],
            };

            this.chart = this.Highcharts.chart(`chart-${this.attr}`, chartOptions);
        },
        expandBox() {
            this.intervalId = setInterval(() => {
                getServerAttrPer(this.serverName, this.attr, this.period).then((res) => {
                    console.log(`Got Data: ${JSON.stringify(res.data.results)}`);

                    /*
                    if (this.hasData) { // update current data
                        // Reverse array, so the newest element will be in position 0.
                        // A little bit faster than array.reverse()...
                        let data = utils.reverseArray(res.data.results);
                        let idx = 0;
                        // Fix date as number of ms passed since epoch.
                        data.forEach((tuple) => { tuple.date = utils.dateToSecEpoch(tuple.date); });

                        let globalData = this.options.series[0].data;
                        if (globalData.length > 0) {
                            // Acha o ultimo cara que eu inseri.
                            while (idx < data.length && data[idx].date !== globalData[globalData.length-1].x) {
                                ++idx;
                            }
                            --idx;
                        } else {
                            idx = data.length - 1;
                        }

                        // Insere todos os dados novos. Se nao tiver dados novos, idx ja vale -1.
                        while (idx > 0) {
                            this.options.series[0].addPoint([ data[idx].date, data[idx].value ], false, true);
                            --idx;
                        }
                    }
                    // If we didnt have data, we already created with correct values, so we will ignore this step.
                    */

                    if (this.hasData) {
                        this.updateData(res.data.results); 
                    }

                    this.hasData = true;
                });
            }, this.interval * 1000);
        },
    },
    watch: {
        expanded(val) {
            if (val) {
                this.expandBox();
            } else {
                if (this.intervalId !== null) {
                    clearInterval(this.intervalId);
                    this.intervalId = null;
                    this.hasData = false;
                }
                this.dataArr = [];
            }
        },
    },
};
</script>

<style>
.box {
    margin-top: 15px;
    border: 1px solid #bababa;
    border-radius: 3px;
}

.expand-icon {
    cursor: pointer;
    font-size: 25px;
    font-weight: normal;
    float: right;
    margin-top: 5px;
    margin-right: 25px;
}

.limit-width {
    max-width: 100%;
}

.limit-width div {
    max-width: 100% !important;
}

.slide-fade-enter-active {
  transition: all .5s ease;

}
.slide-fade-leave-active {
  transition: all .5s ease;
}
.slide-fade-enter, .slide-fade-leave-to
/* .slide-fade-leave-active em versões anteriores a 2.1.8 */ {
  transform: translateY(10px);
  opacity: 0;
}
</style>
