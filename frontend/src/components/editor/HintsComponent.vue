<template>
    <div class="expand layout-center">
        <div class="shortcuts">
            <div class="shortcut-item">
                <div>Run</div>
                <div class="shortcut">
                    <span>{{ icon }}</span><span>Enter</span>
                </div>
            </div>
            <div class="shortcut-item">
                <div>New Tab</div>
                <div class="shortcut">
                    <span>{{ icon }}</span><span>T</span>
                </div>
            </div>
            <div class="shortcut-item">
                <div>Close Tab</div>
                <div class="shortcut">
                    <span>{{ icon }}</span><span>W</span>
                </div>
            </div>
            <div class="shortcut-item">
                <div>Find</div>
                <div class="shortcut">
                    <span>{{ icon }}</span><span>F</span>
                </div>
            </div>
            <div class="shortcut-item">
                <div>Find and Replace</div>
                <div class="shortcut">
                    <span>Ctrl</span><span>H</span>
                </div>
            </div>
        </div>
    </div>
</template>
<style>
.shortcuts {
    display: table;
    border-spacing: 5px;

}

.shortcut-item {
    display: table-row;
    color: var(--text-lighter);
    text-align: right;
    font-size: 95%;
    > div {
    display: table-cell;
  }
  /* .new {
    margin-right: $gutter-h;
  } */
}

.shortcut {
    text-align: left;
    margin-right:5px;
    &>span {
        display: inline-block;
        padding: 0 0.35rem;
        border-radius: 4px;
        font-size: 90%;
        font-weight: normal;
        line-height: 1.6;
        text-align: center;
        white-space: nowrap;
        vertical-align: baseline;
        border: 1px solid gray;
        border-radius: 5px;

        /* background: rgba(var(--main-bg-color), 0.15); */
        background: var(--light-bg-color);
        color: var(--text);
        margin: 0 (var(--gutter-h) * 0.35);
        transition: color 0.15s ease-in-out,
            background-color 0.15s ease-in-out,
            border-color 0.15s ease-in-out,
            box-shadow 0.15s ease-in-out;
    }
}
</style>
<script type="text/javascript">
export default {
    data() {
        return {

        }
    },
    props: {
        'type': {
            sysType: String,
            required: false,
        },
    },
    computed: {
        icon() {
            if (this.sysType == 'mac') {
                return '⌘'
            }
            return 'Ctrl'
        }
    }
}
</script>