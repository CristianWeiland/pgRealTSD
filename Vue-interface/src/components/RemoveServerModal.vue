<template>
    <modal classes="modal-box" name="remove-server-modal">
        <div class="modal-header">
            <button type="button" class="close" aria-hidden="true" @click="cancel()">&times;</button>
            <h4 class="modal-title">Remove Server</h4>
        </div>
        <div class="modal-body form-horizontal">
            <h3>Are you sure you want to <b>remove</b> this server?</h3>
            <br>
            This can not be undone!
        </div>
        <div class="modal-footer">
            <button type="button" class="btn btn-default" @click="cancel()">Cancel</button>
            <button type="button" class="btn btn-danger" @click="submit()">Remove</button>
        </div>
    </modal>
</template>

<script>
export default {
    name: 'remove-server-modal',
    methods: {
        cancel() {
            this.$emit('close');
        },
        submit() {
            this.$emit('removeServer');
            this.$emit('close');
        },
    },
};
</script>
