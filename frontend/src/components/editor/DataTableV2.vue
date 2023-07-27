<template>
    <div class="result-table">
        <div ref="tabulator"></div>
    </div>
</template>

<style>
.result-table {
    display: flex;
    flex-direction: column;
    flex-grow: 1;
    overflow: hidden;

    .tabulator-cell {
        cursor: default;

        &:hover {
            background: transparent;
        }
    }
}
</style>

<script>
import { TabulatorFull } from 'tabulator-tables'
export default {
    data() {
        return {
            tabulator: null,
            actualTableHeight: '100%',
            selectedCell: null
        }
    },
    props: {
        'headers': {
            type: Array,
            required: true,
        },
        'results': {
            type: Array,
            required: true,
        },
    },
    watch: {
        active() {
            if (!this.tabulator) return;
            if (this.active) {
                this.tabulator.restoreRedraw()
                this.$nextTick(() => {
                    this.tabulator.redraw()
                })
            } else {
                this.tabulator.blockRedraw()
            }
        },
        tableData: {
            handler() {
                this.tabulator.replaceData(this.tableData)
            }
        },
        tableColumns: {
            handler() {
                this.tabulator.setColumns(this.tableColumns)
            }
        },
        tableHeight() {
            this.tabulator.setHeight(this.actualTableHeight)
        }
    },
    computed: {
        keymap() {
            const result = {}
            result[this.ctrlOrCmd('c')] = this.copyCell
            return result
        },
        tableData() {
            return this.results
        },

        headerContextMenu() {
            return [
                {
                    label: '<x-menuitem><x-label>Resize all columns to match</x-label></x-menuitem>',
                    action: (_e, column) => {
                        try {
                            this.tabulator.blockRedraw()
                            const columns = this.tabulator.getColumns()
                            columns.forEach((col) => {
                                col.setWidth(column.getWidth())
                            })
                        } catch (error) {
                            console.error(error)
                        } finally {
                            this.tabulator.restoreRedraw()
                        }
                    }
                },
                {
                    label: '<x-menuitem><x-label>Resize all columns to fit content</x-label></x-menuitem>',
                    action: (_e, _column) => {
                        try {
                            this.tabulator.blockRedraw()
                            const columns = this.tabulator.getColumns()
                            columns.forEach((col) => {
                                col.setWidth(true)
                            })
                        } catch (error) {
                            console.error(error)
                        } finally {
                            this.tabulator.restoreRedraw()
                        }
                    }
                },
                {
                    label: '<x-menuitem><x-label>Resize all columns to fixed width</x-label></x-menuitem>',
                    action: (_e, _column) => {
                        try {
                            this.tabulator.blockRedraw()
                            const columns = this.tabulator.getColumns()
                            columns.forEach((col) => {
                                col.setWidth(200)
                            })
                            // const layout = this.tabulator.getColumns().map((c: CC) => ({
                            //   field: c.getField(),
                            //   width: c.getWidth(),
                            // }))
                            // this.tabulator.setColumnLayout(layout)
                            // this.tabulator.redraw(true)
                        } catch (error) {
                            console.error(error)
                        } finally {
                            this.tabulator.restoreRedraw()
                        }
                    }
                }

            ]
        },
        cellContextMenu() {
            return [
                {
                    label: '<x-menuitem><x-label>Copy Cell</x-label></x-menuitem>',
                    action: (_e, cell) => this.$native.clipboard.writeText(cell.getValue())
                },
                {
                    label: '<x-menuitem><x-label>Copy Row (JSON)</x-label></x-menuitem>',
                    action: (_e, cell) => {
                        const data = cell.getRow().getData()
                        const fixed = this.dataToJson(data, true)
                        this.$native.clipboard.writeText(JSON.stringify(fixed))
                    }
                },
                {
                    label: '<x-menuitem><x-label>Copy Row (TSV / Excel)</x-label></x-menuitem>',
                    action: (_e, cell) => this.$native.clipboard.writeText(Papa.unparse([this.$bks.cleanData(cell.getRow().getData())], { header: false, quotes: true, delimiter: "\t", escapeFormulae: true }))
                },
                {
                    label: '<x-menuitem><x-label>Copy Row (Markdown)</x-label></x-menuitem>',
                    action: (_e, cell) => {
                        const data = cell.getRow().getData()
                        const fixed = this.dataToJson(data, true)
                        return this.$native.clipboard.writeText(markdownTable([
                            Object.keys(fixed),
                            Object.values(fixed),
                        ]))
                    }
                },
                {
                    label: '<x-menuitem><x-label>Copy Row (Insert)</x-label></x-menuitem>',
                    action: async (_e, cell) => {
                        const fixed = this.$bks.cleanData(cell.getRow().getData(), this.tableColumns)

                        const tableInsert = {
                            table: 'mytable',
                            schema: null,
                            data: [fixed],
                        }
                        const query = await this.connection.getInsertQuery(tableInsert)
                        this.$native.clipboard.writeText(query)
                    }
                }
            ]
        },
        tableColumns() {
            // const columnWidth = this.result.fields.length > 30 ? globals.bigTableColumnWidth : undefined
            return this.headers.map((column) => {
                const result = {
                    title: column,
                    titleFormatter: 'plaintext',
                    field: column,
                    formatter: this.cellFormatter,
                    tooltip: this.cellTooltip,
                    contextMenu: this.cellContextMenu,
                    headerContextMenu: this.headerContextMenu,
                    cellClick: this.cellClick.bind(this)
                }
                return result;
            })
        }
    },
    beforeDestroy() {
        if (this.tabulator) {
            this.tabulator.destroy()
        }
        document.removeEventListener('click', this.maybeUnselectCell)
    },
    async mounted() {

        this.tabulator = new TabulatorFull(this.$refs.tabulator, {
            // data: this.tableData, //link data to table  
            reactiveData: true,
            renderHorizontal: 'virtual',
            // columns: this.tableColumns, //define table columns

            data: this.tableData, //assign data to table
            columns: this.tableColumns,
            height: this.actualTableHeight,
            nestedFieldSeparator: false,
            clipboard: true,
            keybindings: {
                copyToClipboard: false
            },
            downloadConfig: {
                columnHeaders: true
            }
        });
        document.addEventListener('click', this.maybeUnselectCell)
    },
    methods: {
        maybeUnselectCell(event) {
            if (!this.active) return
            const target = event.target
            if (this.selectedCell) {
                const targets = Array.from(this.selectedCell.getElement().getElementsByTagName("*"))
                if (!targets.includes(target)) {
                    this.selectedCell.getElement().classList.remove('selected')
                    this.selectedCell = null
                }
            }
        },
        copyCell() {
            if (!this.active) return;
            if (!this.selectedCell) return;
            this.selectedCell.getElement().classList.add('copied')
            const cell = this.selectedCell
            setTimeout(() => cell.getElement().classList.remove('copied'), 500)
            this.$native.clipboard.writeText(this.selectedCell.getValue(), false)
        },
        cellClick(e, cell) {
            if (this.selectedCell) {
                this.selectedCell.getElement().classList.remove('selected')
            }
            this.selectedCell = cell
            cell.getElement().classList.add('selected')
        },
        dataToJson(rawData, firstObjectOnly) {
            const rows = _.isArray(rawData) ? rawData : [rawData]
            const result = rows.map((data) => {
                return this.$bks.cleanData(data, this.tableColumns)
            })
            return firstObjectOnly ? result[0] : result
        },
        download(format) {
            let formatter = format !== 'md' ? format : (rows, options, setFileContents) => {
                const values = rows.map(row => row.columns.map(col => col.value))
                setFileContents(markdownTable(values), 'text/markdown')
            };
            formatter = format !== 'json' ? formatter : (rows, options, setFileContents) => {
                setFileContents(
                    JSON.stringify(this.dataToJson(this.tabulator.getData(), false), null, "  "), 'text/json'
                )
            };
            const dateString = dateFormat(new Date(), 'yyyy-mm-dd_hMMss')
            const title = this.query.title ? _.snakeCase(this.query.title) : "query_results"

            const options = typeof formatter !== 'function' && formatter.toLowerCase() === 'xlsx' ? {} : 'all'
            this.tabulator.download(formatter, `${title}-${dateString}.${format}`, options)
        },
        clipboard(format = null) {
            const allRows = this.tabulator.getData()
            if (allRows.length == 0) {
                return
            }
            const columnTitles = {}

            const result = this.dataToJson(allRows, false)

            if (format === 'md') {
                const mdContent = [
                    Object.keys(result[0]),
                    ...result.map((row) => Object.values(row)),
                ];
                this.$native.clipboard.writeText(markdownTable(mdContent))
            } else if (format === 'json') {
                this.$native.clipboard.writeText(JSON.stringify(result))
            } else {
                this.$native.clipboard.writeText(
                    Papa.unparse(
                        result,
                        { header: true, delimiter: "\t", quotes: true, escapeFormulae: true }
                    )
                )
            }
        },
    }
}
</script>
