<template>
    <modal classes="modal-box" name="new-server-modal">
        <div class="modal-header">
            <button type="button" class="close" aria-hidden="true" @click="cancel()">&times;</button>
            <h2 class="modal-title">Add Server</h2>
        </div>
        <div class="modal-body form-horizontal">
            <div class="form-group">
                <div class="col-xs-4 control-label"> Server Name *: </div>
                <div class="col-xs-8">
                    <input class="form-group form-control" :class="{ 'has-error': hasError('name') }"
                        type="text" v-model="server.name" @input="dirty.name = true" @blur="dirty.name = true"/>
                </div>

                <div class="col-xs-4 control-label"> Username *: </div>
                <div class="col-xs-8">
                    <input class="form-group form-control"
                        type="text" v-model="server.username" @input="dirty.username = true"/>
                </div>

                <div class="col-xs-4 control-label"> Password *: </div>
                <div class="col-xs-8">
                    <input class="form-group form-control"
                        type="password" v-model="server.password" @input="dirty.password = true"/>
                </div>
            </div>
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" @click="cancel()">Cancel</button>
            <button type="button" class="btn btn-primary" @click="validate()">Submit</button>
        </div>
    </modal>
</template>

<script>
import { addServer } from '../services/server';

function newServer() {
    return {
        name: '',
        username: '',
        password: '',
    };
}

export default {
    name: 'new-server-modal',
    data() {
        return {
            dirty: {},
            submitted: false,
            server: newServer(),
        };
    },
    methods: {
        hasError(field) {
            if ((this.submitted || this.dirty[field]) && !this.server[field]) return true;
            return false;
        },
        cancel() {
            this.reset();
            this.$emit('close');
        },
        reset() {
            this.dirty = {};
            this.submitted = false;
            this.server = newServer();
        },
        validate() {
            this.submitted = true;
            if (this.hasError('name')) {
                this.$notify({
                    title: 'Error!',
                    text: 'Invalid fields.',
                    type: 'error',
                });
                return;
            }
            this.submit();
        },
        submit() {
            const data = {
                name: this.server.name,
            }

            if (this.server.username) data.user_name = this.server.username;
            if (this.server.password) data.password = this.server.password;

            this.$store.commit('setLoading', true);
            addServer(data).then((res) => {
                console.log(res);
                this.$store.commit('setLoading', false);
                this.$emit('addServer', this.server);
                this.$notify({
                    title: 'Success!',
                    text: 'Server successfully added!',
                    type: 'success',
                });
                this.$emit('close');
                this.reset();
            }).catch((err) => {
                console.log(err);
                this.$store.commit('setLoading', false);
                this.$notify({
                    title: 'Error!',
                    text: 'Internal server error!',
                    type: 'error',
                });
            })
        },
    },
};
</script>

<style>
.has-error {
    border-color: #a94442 !important;
}

.modal-box {
    overflow-y: auto !important;
    height: auto !important;
    min-height: auto !important;
    max-height: 80vh !important;
    /* Default modal style */
    background-color: white;
    text-align: left;
    border-radius: 3px;
    box-shadow: 0 20px 60px -2px rgba(27, 33, 58, 0.4);
    padding: 0;
}
</style>
