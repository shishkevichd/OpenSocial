<template>
    <div class="opensocial_navbar">
        <span class="navbar_title">{{ socialName }}</span>
        <div class="navbar_spacer"></div>
    </div>
</template>

<script>
import packages from "../../package.json"

export default {
    data() {
        return {
            socialName: packages.config.socialname,
        }
    }
}
</script>

<style lang="scss">
.opensocial_navbar {
    display: flex;
    height: 45px;
    width: 100%;
    justify-content: space-between;
    align-items: center;

    .navbar_title {
        font-weight: 600;
    }

    .navbar_spacer {
        width: 1px;
    }
}
</style>