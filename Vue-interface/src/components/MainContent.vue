<template>
    <div>
        <side-menu></side-menu>

        <div v-if="selectedServer && configurations" class="main main-background">
            <app-header :configurations="configurations" :server="selectedServer"></app-header>
            <graphs :server="selectedServer" :configurations="configurations"></graphs>
        </div>

        <div v-if="!selectedServer" class="main main-background" style="padding: 20px">
            <h1 style="margin-top: 0px">Welcome to <b>Online State Detector!</b>
                <span style="float: right">
                    <span style="margin-left: 10px" class="clickable" @click="$router.push({ name: 'configs' })">
                        <span class="glyphicon glyphicon-cog"></span>
                    </span>
                </span>
            </h1>
            <br>
            <p>
                This platform is designed for you to monitor your servers.
                <br><br>
            </p>
            <p v-if="!servers.length">
                In the left menu you will have the list of your servers.<br>
                It looks like you dont have any. You can add a new server in the
                <router-link :to="{ name: 'configs' }">configurations page</router-link>.
            </p>
            <p v-else>
                The left menu has your server list.
                You can select one of your configured servers by clicking on them.
                <br><br>
                After doing so, we will start analyzing the collected data and displaying it to you
                in awesome online charts!
                <br><br>
                If your server does not show any data, make sure it is actively collecting data. You can turn it on/off in the <router-link :to="{ name: 'configs' }">configurations page</router-link>.
            </p>
        </div>
    </div>
</template>

<script type="text/javascript">
import { mapGetters } from 'vuex';

import AppHeader from './AppHeader';
import Graphs from './Graphs';
import SideMenu from './SideMenu';

export default {
    name: 'main-content',
    components: {
        AppHeader,
        Graphs,
        SideMenu,
    },
    computed: {
        ...mapGetters(['servers', 'selectedServer', 'configurations']),
    },
};
</script>
