<template>
    <transition name="fade" mode="out-in">
        <div v-if="!showConfigurations">
            <side-menu
                @selectServer="selectServer"
                @refresh="getServers"
                :servers="servers"
                :serverIdx="selectedServerIdx">
            </side-menu>

            <div class="main main-background">
                <app-header
                    @deselectServer="server = {}"
                    @showConfigs="showConfigurations = true"
                    :configurations="configurations"
                    :server="server"></app-header>

                <graphs :server="server" :configurations="configurations"></graphs>
            </div>
        </div>

        <configurations v-else
            @addServer="(server) => { this.servers.push(server); }"
            @closeConfigs="showConfigurations = false"
            :configurations="configurations"
            :show="showConfigurations"
            :servers="servers">
        </configurations>
    </transition>
</template>

<script>
import Graphs from './Graphs';
import SideMenu from './SideMenu';
import AppHeader from './AppHeader';
import Configurations from './Configurations';
import { getServer, getAllServers } from '../services/server';

export default {
    name: 'main-page',
    components: {
        Graphs,
        SideMenu,
        AppHeader,
        Configurations,
    },
    mounted() {
        this.getServers();
    },
    data() {
        let configs = this.$cookies.get('configurations');
        if (configs) configs = JSON.parse(configs);
        return {
            server: {},
            servers: [],
            selectedServerIdx: 0,
            showConfigurations: false,
            configurations: configs || {
                graphsPerLine: '2',
                period: 5,
                spacing: 3,
                interval: 1,
                maxPoints: 10,
                initializeExpanded: false,
            },
        };
    },
    methods: {
        getServers() {
            getAllServers().then((response) => {
                try {
                    if (!response.status || response.status !== 200) {
                        return this.error('Unable to get servers!');
                    }
                    this.servers = response.data;
                    this.server = this.servers[0];
                    // Test icons:
                    // this.servers[0].state = 'warmup';
                    // this.servers[0].state = 'steady';
                    // this.servers[0].state = 'under_pressure';
                    // this.servers[0].state = 'stress';
                    // this.servers[0].state = 'trashing';
                } catch (e) {
                    console.error(e);
                    this.servers = [];
                    this.error('Unable to get servers!');
                }
            }).catch((err) => {
                console.error(err);
            });
        },
        error(msg) {
            this.$notify({
                title: 'Error!',
                text: msg,
                type: 'error',
            });
        },
        selectServer(idx) {
            getServer(this.servers[idx].name).then((res) => {
                this.serverIdx = idx;
                this.server = res.data;
            });
        },
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

/* Footer */
.footer {
    position: fixed;
    left: 0px;
    bottom: 0px;
    height: 55px;
    width: 100%;
    background-color: #fff;
    border-top: 1px solid #C3C3C3;
}
.footer-btn {
    margin-top: 10px;
    min-width: 300px;
}
</style>