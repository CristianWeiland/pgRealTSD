<template>
    <div class="main-header">
        <div class="config">
            <span style="margin-left: 10px" class="clickable" @click="$emit('showConfigs')">
                <span class="glyphicon glyphicon-cog"></span>
            </span>
        </div>
        <div align="center" class="title">
            <transition name="fade" mode="out-in">
                <span v-if="server && server.name">
                    Server <b>{{server.name}}</b> selected
                    <!-- Removing servers works almost perfectly. The only problem is how to
                    remove all created intervals. -->
                    <!--
                    <span style="margin-left: 10px; margin-top: 5px; font-size: 25px; color: #a94442"
                        class="clickable" @click="$emit('deselectServer')">
                        <span class="glyphicon glyphicon-remove"></span>
                    </span>
                    -->
                </span>
                <p v-else>No server selected. Please choose one from the menu.</p>
            </transition>
        </div>
    </div>
</template>

<script>
export default {
    name: 'app-header',
    props: ['server', 'configurations'],
};
</script>

<style scoped>
.main-header {
    min-height: 50px;
    background-color: #f8f8f8;
    box-shadow: 0 1px 3px 0 rgba(0,0,0,.2);
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .3s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active em versões anteriores a 2.1.8 */ {
  opacity: 0;
}

/* Title Class */
.title {
    padding-left: 10px;
    padding-top: 5px;
    font-size: 30px;
    color: rgba(0, 0, 0, 0.87);
}

.config {
    padding-top: 7px;
    padding-right: 15px;
    font-size: 30px;
    float: right;
}
.back {
    padding: 5px;
    padding-right: 10px;
    font-size: 30px;
    float: left;
}

</style>
