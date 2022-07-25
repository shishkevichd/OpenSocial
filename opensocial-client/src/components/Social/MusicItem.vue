<template>
    <li class="list-group-item music_item">
        <div class="left">
            <i class="bi bi-music-note-beamed"></i>
            <div class="music_meta">
                <span class="music_item_name">Name</span>
                <span class="music_item_artist">Artist</span>
            </div>
        </div>
        <div class="right">
            <ul class="music_item_icons">
                <li class="item_icon"><i class="bi bi-play"></i></li>
                <li class="item_icon"><i class="bi bi-download"></i></li>
                <li class="item_icon"><i class="bi bi-plus-lg"></i></li>
                <li class="item_icon"><i class="bi bi-three-dots-vertical"></i></li>
            </ul>
        </div>
    </li>
</template>

<style lang="scss">
.music_item {
    display: flex;
    justify-content: space-between;
    align-items: center;

    &:nth-child(2) {
        background-color: var(--bs-gray-100);

        &:hover {
            background-color: var(--bs-gray-200);
        }
    }

    &:hover {
        background-color: var(--bs-gray-100);
    }

    .left {
        display: flex;
        align-items: center;

        i.bi {
            margin-right: 20px;
            font-size: 14pt;
        }

        .music_meta {
            display: flex;
            flex-direction: column;

            span.music_item_name {
                color: var(--bs-gray-800);
                font-size: 12pt;
                font-weight: 600;
                margin-right: 5px;
                margin-bottom: -1px;
            }

            span.music_item_artist {
                color: var(--bs-gray-600);
                font-size: 10pt;
            }
        }
    }

    .right {
        .music_item_icons {
            display: flex;
            list-style: none;

            .item_icon {
                margin-right: 14px;

                &:last-child {
                    margin-right: 0;
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