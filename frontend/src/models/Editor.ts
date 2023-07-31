
import { Connection, ConnectionInterface } from '/src/models/Connection'
import { Results, ResultsInterface } from '/src/models/Results'
import axiosHelpers from '/src/api/helpers';
import instance from '/src/api/instance';

export interface EditorInterface {
    name: string;
    type: string;
    connection: string;
    results: ResultsInterface;
    contents: string;
    loading: boolean;
    error: string | null;
    executed: boolean;
}

export interface EditorEnrichedInterface {
    name: string;
    type: string;
    connection: ConnectionInterface;
    results: ResultsInterface;
    contents: string;
    loading: boolean;
    error: string | null;
    executed: boolean;
}

export class Editor implements EditorInterface {
    name: string;
    type: string;
    connection: string;
    results: Results;
    contents: string;
    loading: boolean;
    error: string | null;
    executed: boolean;
    duration: number | null;


    constructor(name: string, type: string, connection: string) {
        this.name = name
        this.type = type
        this.connection = connection
        this.results = new Results([], new Map())
        this.contents = 'SELECT 1 -> echo;'
        this.loading = false;
        this.error = null;
        this.executed = false;
    }
    async runQuery() {
        this.loading = true;
        // this.info = 'Executing query...'
        this.error = null;
        // let current_query = this.editorData.contents;
        this.executed = true;
        let local = this;
        try {
            let info = { connection: local.connection, query: local.contents };
            await instance.post('query', info).then(function (response) {
                const columnMap = new Map();
                for (const [key, value] of response.data.columns) {
                    columnMap.set(key, value);
                }
                local.results = new Results(response.data.results, columnMap); //response.data;
            })
            // this.last_passed_query_text = current_query;
        } catch (error) {
            local.error = axiosHelpers.getErrorMessage(error);
        } finally {
            local.loading = false;
        }
    }

}
