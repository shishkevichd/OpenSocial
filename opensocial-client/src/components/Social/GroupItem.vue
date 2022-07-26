<template>
    <li class="list-group-item opensocial_group_item">
        <div class="left">
            <img :src="group.avatar_url" alt="Avatar">
            <span>{{ group.group_name }}</span>
        </div>
        <div class="right">
            <ul class="group_item_icons">
                <li class="group_item_icon">
                    <i class="bi bi-dash-square"></i>
                </li>
                <li class="group_item_icon">
                    <i class="bi bi-three-dots-vertical"></i>
                </li>
            </ul>
        </div>
    </li>
</template>

<script>
export default {
    props: {
        group: {
            required: true,
            type: Object
        }
    }
}
</script>

<style lang="scss">
.opensocial_group_item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px;

    .left {
        display: flex;
        align-items: center;

        img {
            width: 35px;
            margin-right: 18px;
            border-radius: 4px;
        }

        span {
            font-weight: 600;
        }
    }

    .right {
        .group_item_icons {
            display: flex;
            list-style: none;
            font-size: 14pt;

            .group_item_icon {
                margin-right: 25px;

                &:last-child {
                    margin-right: 5px;
                }

                &:hover {
                    color: var(--bs-primary);
                    cursor: pointer;
                }
            }
        }
    }
}
</style>