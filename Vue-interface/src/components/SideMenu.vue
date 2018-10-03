<template>
    <div class="side-menu">
        <nav class="navbar navbar-default" role="navigation">
            <div class="navbar-header" style="cursor: pointer" :click="$router.push({ name: 'main' })">
                <div class="brand-wrapper">
                    <div class="brand-name-wrapper">
                        <a class="navbar-brand"><b>Online State Detector</b></a>
                    </div>
                </div>
            </div>

            <div class="side-menu-container">
                <br><br><br>
                <ul style="margin-top: -15px; width: 214px" class="nav navbar-nav">
                    <li>
                        <div align="center" class="form-group">
                            <button class="btn btn-default" style="width: 180px">
                                <span
                                  style="color: #333" class="clickable" @click="refresh()">
                                    Refresh Servers &nbsp;<span class="glyphicon glyphicon-refresh"></span>
                                </span>
                            </button>
                        </div>
                    </li>
                    <li>
                        <span class="navbar-form filter">
                            <div class="form-group">
                                <input type="text" class="form-control" style="float: left"
                                       placeholder="Filter Servers" v-model="filter">
                                <div class="clearfix"></div>
                            </div>
                        </span>
                    </li>
                    <li style="height: 12px; border-bottom: 1px solid #bababa"></li>
                    <li style="padding: 15px; background-color: #455062">
                      <div v-for="(server, index) in filteredServers" :key="index"
                        class="server-box" @click="selectServer(index)">
                          <a style="display: grid; grid-template-columns: auto 1fr auto; color: #282828; text-decoration: none" href="#">
                              <span class="glyphicon" :class="[getIcon(server.state)]" style="top: 3px"
                                v-tooltip.top-center="statusTip(server.state)">
                              </span>
                              <span>{{server.name}}</span>
                              <span class="color-box" :class="[ server.active ? 'blue' : 'grey' ]"
                                style="margin-top: 8px"></span>
                          </a>
                      </div>
                    </li>
                </ul>
            </div>
        </nav>
    </div>
</template>

<script type="text/javascript">
import { mapGetters } from 'vuex';

import { getServer, getAllServers } from '../services/server';

export default {
    name: 'side-menu',
    props: [],
    data() {
        return {
            server: {},
            filter: '',
            loading: this.$store.state.loading,
        };
    },
    computed: {
        ...mapGetters(['servers', 'selectedServerIndex']),
        filteredServers() {
            const f = this.filter.toLowerCase();
            if (!this.filter) return this.servers;
            return this.servers.filter((server) => {
                return server.name.toLowerCase().indexOf(f) !== -1;
            });
        },
    },
    mounted() {
        this.getServers();
    },
    methods: {
        statusTip(status) {
            if (status === 'warmup') return 'Server is initializing...';
            if (status === 'steady') return 'Server is steady! Nice!';
            if (status === 'under_pressure') return 'Server is getting under pressure... Keep an eye on it!';
            if (status === 'stress') return 'Server is stressed! Please do something!';
            if (status === 'trashing') return 'Server is going to die. You have failed this city!';
        },
        getIcon(status) {
            let icon = '';
            if (status === 'warmup') icon = 'plane';
            if (status === 'steady') icon = 'thumbs-up';
            if (status === 'under_pressure') icon = 'scale';
            if (status === 'stress') icon = 'warning-sign';
            if (status === 'trashing') icon = 'trash';
            return `glyphicon-${icon}`;
        },
        selectServer(idx) {
            this.$store.commit('setLoading', true);
            getServer(this.servers[idx].name).then((res) => {
                this.$store.commit('setLoading', false);
                this.$store.commit('selectServer', { server: res.data, idx });
            }).catch((err) => {
                console.log(err);
                this.error(`Unable to get server ${this.servers[idx].name}!`);
                this.$store.commit('setLoading', false);
            });
        },
        refresh() {
            if (this.loading && this.loading.show) return;
            this.$store.commit('setLoading', true);
            this.getServers(true);
        },
        getServers(isRefresh) {
            getAllServers().then((response) => {
                try {
                    if (!response.status || response.status !== 200) {
                        return this.error('Unable to get servers!');
                    }
                    this.$store.commit('setServers', response.data);
                    if (response.data.length) {
                        this.selectServer(0);
                    }
                    // Test icons:
                    // this.servers[0].state = 'warmup';
                    // this.servers[0].state = 'steady';
                    // this.servers[0].state = 'under_pressure';
                    // this.servers[0].state = 'stress';
                    // this.servers[0].state = 'trashing';
                    if (isRefresh) {
                        this.$notify({
                            title: 'Success!',
                            text: 'Servers refreshed successfully.',
                            type: 'success',
                        });
                    }
                } catch (e) {
                    console.error(e);
                    this.error('Unable to get server list. Please contact the admin!');
                }
                this.$store.commit('setLoading', false);
            }).catch((err) => {
                this.error('Unable to get server list. Please contact the admin!');
                this.$store.commit('setLoading', false);
                console.error(err);
            });
        },
    },
};
</script>

<style scoped>
/* Side Menu Stuff */
.filter {
    min-width: 2000px;
}
.side-menu {
  position: fixed;
  width: 215px;
  height: 100%;
  /* Dark Menu */
  background-color: #455062;
  color: rgba(255, 255, 255, 0.7);
  border-right: 1px solid #C3C3C3;
  overflow-y: auto;
}
.side-menu .navbar {
  /*background-color: #455062;*/
  background-color: #F8F8F8;
  border: none;
}
.side-menu .navbar-header {
  width: 100%;
  box-shadow: 0 1px 3px 0 rgba(0,0,0,.2);
}
.side-menu .navbar-nav .active a {
  background-color: transparent;
  margin-right: -1px;
  border-right: 5px solid #e7e7e7;
}
.side-menu .navbar-nav li {
  display: block;
  width: 100%;
}
.side-menu .brand-name-wrapper {
  min-height: 50px;
  background-color: #33A1DE;
}
.side-menu .brand-name-wrapper .navbar-brand {
  color: #E5E5E5;
  display: block;
}
.side-menu #search {
  position: relative;
  z-index: 1000;
}
.side-menu #search .panel-body {
  padding: 0;
}
.side-menu #search .panel-body .navbar-form {
  background-color: #FFFFFF;
  padding: 0;
  padding-right: 50px;
  width: 90%;
  margin: 0;
  position: relative;
  border-top: 1px solid #e7e7e7;
}
.side-menu #search .panel-body .navbar-form .form-group {
  width: 100%;
  position: relative;
}
.side-menu #search .panel-body .navbar-form input {
  border: 0;
  border-radius: 0;
  box-shadow: none;
  width: 100%;
  height: 50px;
}
.side-menu #search .panel-body .navbar-form .btn {
  position: absolute;
  right: 0;
  top: 0;
  border: 0;
  border-radius: 0;
  background-color: #F8F8F8;
  padding: 15px 18px;
}
.side-menu-text-color {
  color: #e7e7e7;
}

.server-box {
  cursor: pointer;
  padding: 10px;
  background-color: #fff;
  margin-bottom: 15px;
  border-radius: 10px;
}

.server-box:hover {
  background-color: #dedede;
}


</style>
