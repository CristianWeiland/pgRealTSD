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
import moment from 'moment';

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
            dataArr: [],
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
                        text: utils.capitalize(this.hrAttr),
                    },
                    plotLines: [{
                        value: 0,
                        width: 1,
                        color: '#808080'
                    }],
                },
                tooltip: {
                    formatter: function() {
                        return `Attr: <b>${vm.hrAttr}</b><br/>Time: ${this.x}<br/>Value: ${this.y}`;
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
                    /* Res.data format:
                    res.data = [
                        { date: "11/04/2018 19:20:20", value: 855156},
                        { date: "11/04/2018 19:20:23", value: 858460}
                    ]*/
                    /* Explicação: Procura o ponto p mais recente do gráfico.
                    Filtra dados recebidos, pegando só dados mais recentes que p (são dados novos).
                    Ordena os dados novos.
                    Chama addPoint pra todos os dados novos na ordem correta. */
                    const format = 'dd/MM/YYYY HH:mm:ss';
                    const n = this.configurations.maxPoints;
                    let pointsToAdd = res.data;
                    const currentData = this.chart.series[0].data;
                    // If we have no data, we just add whatever we got from this call.
                    if (currentData.length > 0) {
                        // Get the most recent date in our current graph
                        let latest = currentData.reduce((best, elem) => {
                            if (!best) return elem;
                            if (moment(elem.x, format).isBefore(moment(best.x, format))) {
                                return best;
                            }
                            return elem;
                        }, null);
                        latest = moment(latest.x);

                        // Get only points that are more recent than our graph's points.
                        pointsToAdd = pointsToAdd.filter((elem) => {
                            return moment(elem.date, format).isAfter(latest);
                        });

                        // Sort data
                        pointsToAdd.sort((a, b) => {
                            if (moment(a.date, format).isAfter(moment(b.date, format))) return 1;
                            if (moment(b.date, format).isAfter(moment(a.date, format))) return -1;
                            return 0;
                        });
                    }

                     // If we received more points than we want to show, cut them off.
                    if (pointsToAdd.length > n) {
                        pointsToAdd = pointsToAdd.slice(-n);
                    }

                    pointsToAdd.forEach((elem) => {
                        const shift = currentData.length >= n;
                        // Highcharts expects data to be formatted in ms since epoch.
                        const msSinceEpoch = moment(elem.date, format).valueOf();
                        this.chart.series[0].addPoint([msSinceEpoch, elem.value], true, shift);
                    });
                });
            }, this.interval * 3000);
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
