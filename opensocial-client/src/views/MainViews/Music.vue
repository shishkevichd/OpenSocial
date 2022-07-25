<template>
    <div class="mb-3">
        <div class="input-group mb-3">
            <input type="search" class="form-control" placeholder="Поиск музыки" v-model="searchQuery">
        </div>
    </div>
    <div class="mb-3" v-if="searchQuery.length <= 0">
        <h4 class="mb-3">Ваша музыка</h4>
        <ul class="list-group">
            <music-item-vue />
            <music-item-vue />
            <music-item-vue />
        </ul>
    </div>
    <div class="mb-3" v-else>
        <h4 class="mb-3">Поиск по запросу "{{ searchQuery }}"</h4>
        <ul class="list-group">
            <music-item-vue />
        </ul>
    </div>
</template>

<script>
import MusicItemVue from "../../components/Social/MusicItem.vue";

export default {
    data() {
        return {
            searchQuery: ""
        }
    },
    components: {
        MusicItemVue
    }
}
</script>