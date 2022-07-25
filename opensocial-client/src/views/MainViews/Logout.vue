<template>
    <div class="text-center">
        <h5 class="my-5">Выход из аккаунта</h5>
        <div class="spinner-border" role="status">
            <span class="visually-hidden">Loading...</span>
        </div>
    </div>
</template>

<script>
export default {
    mounted() {
        localStorage.clear()

        window.location.reload()
    }
}
</script>