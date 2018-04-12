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
            // dataArr: [0, 1],
            dataArr: [],
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
                        /* TODO: Parse time
                        return '<b>' + this.attr + '</b><br/>Time: ' +
                            this.Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +
                            '<br/>Value: ' + this.y;
                        */
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
                    /* V1 (não funciona):
                    console.log(res.data);
                    const a = this.dataArr;
                    const b = res.data;
                    const result = [];
                    let i = 0, j = 0;
                    while (i < a.length && j < b.length) {
                        // TODO: Tem qeu usar moment nessa comparação
                        if (a[i].date === b[j].date) {
                            result.push(a[i].value);
                            i += 1;
                            j += 1;
                        } else if (a[i].date > b[j].date) {
                            result.push(b[j].value);
                            j += 1;
                        } else { // a[i].date < b[j].date
                            result.push(a[i].value);
                            i += 1;
                        }
                    }
                    while (i < a.length) {
                        result.push(a[i].value);
                        i += 1;
                    }
                    while (j < b.length) {
                        result.push(b[j].value);
                        j += 1;
                    }
                    // TODO: Arrumar reverseArray (tem que usar moment no result[i].date)
                    let data = utils.reverseArray(result);
                    if (data.length > this.configurations.maxPoints) {
                        data = data.slice(this.configurations.maxPoints);
                    }
                    // Isso não vai funcionar enquanto não tiver maxPoints elementos! Vai duplicar!
                    data.forEach((elem) => {
                        const shift = this.chart.series[0].data.length >= this.configurations.maxPoints;
                        this.chart.series[0].addPoint([elem.value, elem.date], true, shift);
                    });
                    */
                    /* V2: */
                    /*
                    const a = this.dataArr;
                    const b = res.data;
                    const n = this.configurations.maxPoints;
                    const f = 'dd/MM/YYYY HH:mm:ss';
                    let result = [];
                    let i = 0, j = 0;
                    while (i < a.length && j < b.length) {
                        // TODO: Tem que usar moment nessa comparação
                        if (moment(a[i].date, f) === moment(b[j].date, f)) {
                            result.push(a[i]);
                            i += 1;
                            j += 1;
                        } else if (a[i].date > b[j].date) {
                            result.push(b[j]);
                            j += 1;
                        } else { // a[i].date < b[j].date
                            result.push(a[i]);
                            i += 1;
                        }
                    }
                    while (i < a.length) {
                        result.push(a[i]);
                        i += 1;
                    }
                    while (j < b.length) {
                        result.push(b[j]);
                        j += 1;
                    }
                    // TODO: Arrumar reverseArray (tem que usar moment no result[i].date)
                    // let data = reverseArray(result);
                    result.sort((a, b) => {
                        if (moment(a.date, f).isAfter(moment(b.date, f))) return 1;
                        if (moment(b.date, f).isAfter(moment(a.date, f))) return -1;
                        return 0;
                    });
                    if (result.length > n) {
                        result = result.slice(-n);
                        result.forEach((elem) => {
                            // const shift = this.chart.series[0].result.length >= n;
                            // I have enough points to remake the whole graphic, so shift will always be true.
                            console.log('adding point...');
                            console.log(elem.value, elem.date);
                            this.chart.series[0].addPoint([elem.value, elem.date], true, true);
                        });
                    } else {
                        // We dont have enough points to fill the whole graphic.
                        // So we should try to remove all points and insert all of 'result' again.
                    }
                    console.log('Final result:');
                    console.log(result);

                    /*
                    result.forEach((elem) => {
                        const shift = this.chart.series[0].result.length >= n;
                        this.chart.series[0].addPoint([elem.value, elem.date], true, shift);
                    });
                    */


                    /* V3: Procura o ponto p mais recente do gráfico.
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
                            if (moment(a.date, f).isAfter(moment(b.date, f))) return 1;
                            if (moment(b.date, f).isAfter(moment(a.date, f))) return -1;
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

                    /*
                    O raciocínio vai ser algo mais ou menos como o algoritmo de Merge do
                    Merge Sort. Tenho dois arrays, a e b, correspondendo aos dados já existentes
                    de um gráfico e aos dados novos que chegaram, e dois índices, i e j, cada um
                    percorrendo cada array.
                    Comparo os dois timestamps:
                    while (i < a.length && j < b.length)
                    - Se a[i].date === b[j].date, insiro o dado de qualquer um dos arrays e
                      incremento os dois índices;
                    - Se a[i] > b[j], result.push(b[j].value), j++;
                    - Se a[i] < b[j], result.push(a[i].value), i++;
                    Quando acabou, termina de inserir quem faltou do array que não acabou:
                    while (i < a.length) result.push(a[i].value);
                    while (j < b.length) result.push(b[j].value);
                    Depois de inserir todos os elementos, inverte o array e corta, deixando apenas
                    this.configurations.maxPoints elementos.
                    Insere todos os elementos com addPoint e shift = this.chart.series[0].data.length >= this.configurations.maxPoints.
                    */

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
                    /*
                    if (this.hasData) {
                        this.updateData(res.data.results); 
                    }

                    this.hasData = true;
                    */
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
