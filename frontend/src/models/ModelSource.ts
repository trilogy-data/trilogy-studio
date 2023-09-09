

export interface ModelSourceInterface {
    editor: string,
}


export class ModelSource implements ModelSourceInterface {
    editor: string
    alias: string | null


    constructor(editor: string, alias: string | null) {
        this.editor = editor
        this.alias = alias
    }


    static fromJSON({ editor, alias}): ModelSource {
        let output = new ModelSource(editor, alias);
        return output
    }


}
