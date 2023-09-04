

export interface ModelSourceInterface {
    editor: string,
}


export class ModelSource implements ModelSourceInterface {
    editor: string


    constructor(editor: string) {
        this.editor = editor
    }


    static fromJSON({ editor }): ModelSource {
        let output = new ModelSource(editor);
        return output
    }


}
