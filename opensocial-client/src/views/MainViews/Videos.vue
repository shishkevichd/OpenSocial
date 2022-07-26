<template>
    <div class="mb-3">
        <div class="input-group mb-3">
            <input type="search" class="form-control" placeholder="Поиск видео">
        </div>
    </div>
    <div class="mb-3">
        <div class="opensocial_your_video_header mb-3">
            <h4>Ваши видеозаписи</h4>
            <button class="btn btn-sm btn-primary">Новое видео</button>
        </div>
        <div class="row">
            <div class="col-sm-12 col-md-6 col-xl-4">
                <video-card-vue />
            </div>
            <div class="col-sm-12 col-md-6 col-xl-4">
                <video-card-vue />
            </div>
            <div class="col-sm-12 col-md-6 col-xl-4">
                <video-card-vue />
            </div>
            <div class="col-sm-12 col-md-6 col-xl-4">
                <video-card-vue />
            </div>
        </div>
    </div>
</template>

<script>
import VideoCardVue from "../../components/Social/VideoCard.vue";

export default {
    components: {
        VideoCardVue
    }
}
</script>

<style lang="scss">
.opensocial_your_video_header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    > h4 {
        margin: 0;
    }
}
</style>