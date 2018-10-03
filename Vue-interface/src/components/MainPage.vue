<template>
    <div>
        <router-view></router-view>
    </div>
</template>

<script>

export default {
    name: 'main-page',
    created() {
        let configs = this.$cookies.get('configurations');
        if (configs) {
            configs = JSON.parse(configs);
        } else {
            configs = {
                graphsPerLine: '2',
                period: 5,
                spacing: 3,
                interval: 1,
                maxPoints: 10,
                initializeExpanded: false,
            };
        }
        this.$store.commit('setConfigs', configs);
    },
};
</script>

<style>
body {
    font-size: 18px;
}

.main {
    margin: 0px;
    margin-left: 215px; /* Ou 20%. Se for 20%, mudar o Width de .side-menu também. */
}
.main-background {
    background-color: #e5e5e5;
}
.graph-width {
    width: 99%;
}

/* Page Navigation Classes */
.config-animation {
    transition: all linear 0.5s;
}
.back {
    padding: 5px;
    padding-right: 10px;
    font-size: 30px;
    float: left;
}

/* General classes */
.clickable {
    cursor: pointer;
}
.capitalize {
    text-transform: capitalize;
}
.content {
    padding-top: 30px;
    padding-bottom: 55px;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .4s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active em versões anteriores a 2.1.8 */ {
  opacity: 0;
}


/* Status Squares */
.color-box {
    width: 10px;
    height: 10px;
    margin: 5px;
    margin-left: 0px;
    float: right;
    border-radius: 5px;
}
.blue {
    border: 1px solid #00BFFF;
    background-color: #00BFFF;
}
.grey {
    border: 1px solid #708090;
    background-color: #708090;
}

/* Graph Box */
.outer-graph-frame {
    padding: 10px;
}

/* Config Page Classes */
.table-width {
    width: 80%;
}
.table-background {
    background-color: #ffffff;
}
.small-column {
    width: 120px;
}
.smallest-column {
    width: 1%;
}
</style>