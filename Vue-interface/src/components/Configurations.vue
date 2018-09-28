<template>
    <div>
        <new-server-modal
            @close="toggleNewServerModal()"
            @addServer="(server) => { this.$emit('addServer', server); }">
        </new-server-modal>

        <remove-server-modal
            @close="toggleRemoveServerModal()"
            @removeServer="removeServer">
        </remove-server-modal>

        <div class="back">
            <span class="clickable" @click="$emit('closeConfigs')">
                <span class="clickable glyphicon glyphicon-arrow-left"></span>
            </span>
        </div>
        <div align="center" class="title"></div>
        <div class="content" align="center">
            <table v-if="!empty" class="table table-width table-bordered table-striped table-background">
                <thead>
                    <tr>
                        <th>#</th>
                        <th>Server</th>
                        <th>Username</th>
                        <th>Status</th>
                        <th>Turn On/Off</th>
                        <th class="small-column">Remove</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="(server, index) in servers" :key="index">
                        <th>{{index+1}}</th>
                        <th>{{server.name}}</th>
                        <th>{{server.user_name}}</th>
                        <th class="capitalize">
                            {{ server.active ? 'Collecting - ' + server.state : 'Not Collecting' }}
                        </th>
                        <th style="padding-left: 39px" class="small-column">
                            <button class="btn btn-default" @click="turn(index)"><span class="glyphicon glyphicon-off"></span></button>
                        </th>
                        <th style="padding-left: 22px" class="smallest-column">
                            <button class="btn btn-default" @click="toggleRemoveServerModal(server, index)"><span class="glyphicon glyphicon-trash"></span></button>
                        </th>
                    </tr>
                </tbody>
            </table>
            <div v-else>
                You dont have any servers registered. Please, register them in the button below.
            </div>
        </div>

        <div style="margin-bottom: 85px" class="box col-xs-8 col-xs-offset-2">
            <div style="margin-bottom: 25px; margin-top: 5px" class="col-xs-8">Number of graphs per line:</div>
            <div class="col-xs-4">
                <select class="form-control" v-model="configurations.graphsPerLine" @blur="dirty = true">
                    <option value="1">1</option>
                    <option value="2">2</option>
                    <option value="3">3</option>
                </select>
            </div>

            <div style="margin-bottom: 25px" class="col-xs-8">Period to analyze data (minutes):</div>
            <div class="col-xs-4">
                <input @blur="dirty = true" class="form-control" type="number" min="1" max="30" v-model="configurations.period"/>
            </div>

            <div style="margin-bottom: 25px" class="col-xs-8">Spacing between data (in number of values). For example, 3 means every 3 values in database we return 1:</div>
            <div class="col-xs-4">
                <input @blur="dirty = true" class="form-control" type="number" min="1" max="10" v-model="configurations.spacing"/>
            </div>

            <div style="margin-bottom: 25px" class="col-xs-8">Interval to get new data (seconds):</div>
            <div class="col-xs-4">
                <input @blur="dirty = true" class="form-control" type="number" min="1" max="30" v-model="configurations.interval"/>
            </div>

            <div style="margin-bottom: 25px" class="col-xs-8">Maximum number of points in each graph:</div>
            <div class="col-xs-4">
                <input @blur="dirty = true" class="form-control" type="number" min="2" max="1000" v-model="configurations.maxPoints"/>
            </div>

            <!-- This works, but has two problems:
                1. Checkbox style;
                2. Performance issues when loading all graphs simultaneously;
            <div style="margin-bottom: 25px" class="col-xs-8">Initialize with graphs expanded:</div>
            <div class="col-xs-4">
                <input @blur="dirty = true" class="form-control" type="checkbox" v-model="configurations.initializeExpanded"/>
            </div>
            -->

            <div class="col-xs-12">
                <button :disabled="!dirty" @click="saveConfigs" class="btn btn-default">Save changes</button>
            </div>
        </div>

        <div class="footer">
            <div align="center">
                <button @click="toggleNewServerModal(this)" class="btn btn-primary footer-btn"><span class="glyphicon glyphicon-plus"></span> Add Server</button>
            </div>
        </div>
    </div>
</template>

<script>
import NewServerModal from './NewServerModal';
import RemoveServerModal from './RemoveServerModal';

import { activateServer, deleteServer } from '../services/server';

export default {
    name: 'configurations',
    components: {
        NewServerModal,
        RemoveServerModal,
    },
    props: ['servers'],
    data() {
        return {
            configurations: this.$store.state.configurations,
            showingNewServerModal: false,
            showingRemoveServerModal: false,
            removeIdx: -1,
            dirty: false,
        };
    },
    computed: {
        empty() {
            return !this.servers || !this.servers.length;
        },
    },
    methods: {
        success(msg) {
            this.$notify({ title: 'Success!', text: msg, type: 'success' });
        },
        error(msg) {
            this.$notify({ title: 'Error!', text: msg, type: 'error' });
        },
        turn(idx) {
            activateServer(this.servers[idx].name).then((res) => {
                console.log(res);
                this.$set(this.servers[idx], 'active', !this.servers[idx].active);
                this.success(`Server ${this.servers[idx].active ? '' : 'de'}activated succesfully!`);
            }).catch(() => {
                this.error(`Unable to ${this.servers[idx].active ? '' : 'de'}activate server!`);
            });
        },
        saveConfigs() {
            this.success('Configurations saved successfully!');
            this.$cookies.set('configurations', JSON.stringify(this.configurations));
            this.$store.commit('setConfigs', this.configurations);
            this.dirty = false;
        },
        removeServer() {
            const idx = this.removeIdx;
            if (idx === -1) return;
            this.removeIdx = -1;
            this.$store.commit('setLoading', true);
            deleteServer(this.servers[idx].name).then(() => {
                this.servers.splice(idx, 1);
                this.success('Server removed succesfully!');
                this.$store.commit('setLoading', false);
            }).catch((err) => {
                console.log(err);
                this.error('Unable to remove server. Try again later.');
                this.$store.commit('setLoading', false);
            })
        },
        toggleNewServerModal(server) {
            if (this.showingNewServerModal) {
                this.$modal.hide('new-server-modal');
            } else {
                this.$modal.show('new-server-modal', server);
            }
            this.showingNewServerModal = !this.showingNewServerModal;
        },
        toggleRemoveServerModal(server, idx) {
            if (this.showingRemoveServerModal) {
                this.$modal.hide('remove-server-modal');
            } else {
                this.removeIdx = idx;
                this.$modal.show('remove-server-modal', server);
            }
            this.showingRemoveServerModal = !this.showingRemoveServerModal;
        },
    }
};
</script>

<style scoped>
.box {
    border: 1px solid #bababa;
    border-radius: 3px;
    box-shadow: 1px 1px rgba(0,0,0,0.2);
    padding-top: 25px;
    padding-bottom: 15px;
    background-color: rgba(0,0,0,0.05);
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
