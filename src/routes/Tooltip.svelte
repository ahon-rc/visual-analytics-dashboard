<script>
    let {evt, offset = -35, children} = $props()
</script>

<style>
    .tooltip {
        position: absolute;
        width: 150px;
        border: 1px solid #ccc;
            font-size: 13px;
        background: rgba(255, 255, 255, 0.85);
        transform: translate(-50%, -100%);
        padding: 5px;
        z-index: 15;
    }
</style>

{#if evt.detail}
    <div
        class="tooltip"
        style="
        top:{evt.detail.e.layerY + offset}px;
        left:{evt.detail.e.layerX}px;
        "
    >
            {console.log(evt.detail)}
        {@render children?.({ detail: evt.detail, })}
    </div>
{/if}
