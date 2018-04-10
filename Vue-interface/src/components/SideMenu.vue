<template>
    <div class="side-menu">
        <nav class="navbar navbar-default" role="navigation">
            <div class="navbar-header">
                <div class="brand-wrapper">
                    <div class="brand-name-wrapper">
                        <a class="navbar-brand"><b>DSMPN</b></a>
                    </div>
                </div>
            </div>

            <div class="side-menu-container">
                <br><br><br>
                <ul style="margin-top: -15px; width: 215px" class="nav navbar-nav">
                    <li>
                        <div align="center" class="form-group">
                            <button class="btn btn-default" style="width: 180px">
                                <span style="color: #333" class="clickable" @click="$emit('refresh')">
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
                    <li v-for="(server, index) in filteredServers" :key="index">
                        <a style="color: #282828" href="#" @click="selectServer(index)">
                            <span
                              class="glyphicon" :class="[getIcon(server.state)]"
                              v-tooltip.top-center="statusTip(server.state)">
                            </span>
                            {{server.name}}
                            <span class="color-box" :class="[ server.active ? 'blue' : 'grey' ]"></span>
                        </a>
                    </li>

                </ul>
            </div>
        </nav>
    </div>
</template>

<script type="text/javascript">
export default {
    name: 'side-menu',
    props: ['servers', 'serverIdx'],
    data() {
        return {
            server: {},
            filter: '',
        };
    },
    computed: {
        filteredServers() {
            const f = this.filter.toLowerCase();
            if (!this.filter) return this.servers;
            return this.servers.filter((server) => {
                return server.name.toLowerCase().indexOf(f) !== -1;
            });
        },
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
            this.$emit('selectServer', idx);
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
  /*background-color: #FFFFFF; /* Background in the empty space (below the server list) */
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
  /*border-bottom: 1px solid #e7e7e7;*/
}
.side-menu .navbar-nav li a {
  padding: 15px;
}
.side-menu .navbar-nav li a:hover {
  /*background-color: rgba(59,70,88,0.87);*/
  /*background-color: rgba(255,255,255,0.87);*/
  background-color: #dbdbdb; /* Color when hovering */
}
.side-menu .brand-name-wrapper {
  min-height: 50px;
  background-color: #33A1DE; /* Makes DSMPN background blue. Removing turns it the same color as the rest of the sidebar.. */
  /*background-color: #e5e5e5;*/
}
.side-menu .brand-name-wrapper .navbar-brand {
  /*color: #282828; DSMPN color */
  color: #E5E5E5;
  /*color: #424242;*/
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
  /*background-color: #455062;*/
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
  /*background-color: #f3f3f3;*/
  /*background-color: #455062;*/
  background-color: #F8F8F8;
  padding: 15px 18px;
}
.side-menu-text-color {
  color: #e7e7e7;
}
/* small screen */
@media (max-width: 768px) {
  .side-menu {
    position: relative;
    width: 100%;
    height: 0;
    border-right: 0;
    border-bottom: 1px solid #e7e7e7;
  }
  .side-menu .brand-name-wrapper .navbar-brand {
    display: inline-block;
  }
  /* Slide in animation */
  @-moz-keyframes slidein {
    0% {
      left: -300px;
    }
    100% {
      left: 10px;
    }
  }
  @-webkit-keyframes slidein {
    0% {
      left: -300px;
    }
    100% {
      left: 10px;
    }
  }
  @keyframes slidein {
    0% {
      left: -300px;
    }
    100% {
      left: 10px;
    }
  }
  @-moz-keyframes slideout {
    0% {
      left: 0;
    }
    100% {
      left: -300px;
    }
  }
  @-webkit-keyframes slideout {
    0% {
      left: 0;
    }
    100% {
      left: -300px;
    }
  }
  @keyframes slideout {
    0% {
      left: 0;
    }
    100% {
      left: -300px;
    }
  }
  /* Slide side menu*/
  /* Add .absolute-wrapper.slide-in for scrollable menu -> see top comment */
  .side-menu-container > .navbar-nav.slide-in {
    -moz-animation: slidein 300ms forwards;
    -o-animation: slidein 300ms forwards;
    -webkit-animation: slidein 300ms forwards;
    animation: slidein 300ms forwards;
    -webkit-transform-style: preserve-3d;
    transform-style: preserve-3d;
  }
  .side-menu-container > .navbar-nav {
    /* Add position:absolute for scrollable menu -> see top comment */
    position: fixed;
    left: -300px;
    width: 300px;
    top: 43px;
    height: 100%;
    border-right: 1px solid #e7e7e7;
    /*background-color: #f8f8f8;*/
    /*background-color: #455062;
    color: rgba(255, 255, 255, 0.7);*/
    background-color: #FFFFFF;
    color: rgba(69,80,98,0.7);
    -moz-animation: slideout 300ms forwards;
    -o-animation: slideout 300ms forwards;
    -webkit-animation: slideout 300ms forwards;
    animation: slideout 300ms forwards;
    -webkit-transform-style: preserve-3d;
    transform-style: preserve-3d;
  }
  /* Uncomment for scrollable menu -> see top comment */
  /*.absolute-wrapper{
        width:285px;
        -moz-animation: slideout 300ms forwards;
        -o-animation: slideout 300ms forwards;
        -webkit-animation: slideout 300ms forwards;
        animation: slideout 300ms forwards;
        -webkit-transform-style: preserve-3d;
        transform-style: preserve-3d;
    }*/
  /* Search */
  #search .panel-body .navbar-form {
    border-bottom: 0;
  }
  #search .panel-body .navbar-form .form-group {
    margin: 0;
  }
  .navbar-header {
    /* this is probably redundant */
    position: fixed;
    z-index: 3;
    /*background-color: #f8f8f8;*/
    /*background-color: #455062;*/
    background-color: #FFFFFF;
  }
}

</style>
