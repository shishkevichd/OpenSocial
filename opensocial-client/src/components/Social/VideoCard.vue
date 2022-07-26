<template>
    <div class="card opensocial_video_card mb-3">
        <svg class="bd-placeholder-img card-img-top" width="100%" height="180" xmlns="http://www.w3.org/2000/svg"
            role="img" aria-label="Placeholder: Image cap" preserveAspectRatio="xMidYMid slice" focusable="false">
            <title>Placeholder</title>
            <rect width="100%" height="100%" fill="#868e96"></rect><text x="50%" y="50%" fill="#dee2e6" dy=".3em">Image
                cap</text>
        </svg>
        <div class="card-body">
            <span class="body_name">Title</span>
            <span class="body_author">Author</span>
            <span class="body_viewers_and_date">3K просмотров • Сегодня</span>
        </div>
    </div>
</template>

<style lang="scss">
.opensocial_video_card {
    border: none;

    .card-img-top {
        border-radius: 4px;

        &:hover {
            filter: drop-shadow(0 20px 13px rgb(0 0 0 / 0.03)) drop-shadow(0 8px 5px rgb(0 0 0 / 0.08));
            cursor: pointer;
        }
    }

    .card-body {
        display: flex;
        flex-direction: column;
        padding: 0;

        .body_name {
            font-weight: 600;
            margin-top: 7px;
            font-size: 13pt;
        }
        .body_author, .body_viewers_and_date {
            font-size: 11pt;
            color: var(--bs-gray-600);
        }
    }
}
</style>