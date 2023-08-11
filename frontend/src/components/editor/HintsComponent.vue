<template>
    <div class="expand layout-center hints">
        <div class="shortcuts">
            <div v-for="shortcut in shortcuts" class="shortcut-item">
                <div>{{ shortcut.name }}</div>
                <div class="shortcut">
                    <span>{{ icon }}</span><span v-for="key in shortcut.keys">{{ key }}</span>
                </div>
            </div>
        </div>
    </div>
</template>
<style>
.hints {
    height: 100%;
}

.shortcuts {
    display: table;
    border-spacing: 5px;

}

.shortcut-item {
    display: table-row;
    color: var(--text-lighter);
    text-align: right;
    font-size: 95%;

    >div {
        display: table-cell;
    }

    /* .new {
    margin-right: $gutter-h;
  } */
}

.shortcut {
    text-align: left;
    margin-right: 5px;

    &>span {
        display: inline-block;
        padding: 0 0.35rem;
        border-radius: 4px;
        margin-right: .35rem;
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
            shortcuts: [
                {
                    name: 'Run',
                    keys: ['Enter']
                },
                {
                    name: 'Save Open Editor',
                    keys: ['S']
                },
                {
                    name: 'New Tab',
                    keys: ['T']
                },
                {
                    name: 'Close Tab',
                    keys: ['W']
                },
                {
                    name: 'Find',
                    keys: ['F']
                },
                {
                    name: 'Find and Replace',
                    keys: ['H']
                }
            ]

        }
    },
    props: {
        'sysType': {
            type: String,
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