

export interface LineageItemInterface {
    token: string,
    depth: number,
    link: string | null
}




export class LineageItem implements LineageItemInterface {
    token: string
    depth: number
    link: string | null


    constructor(token: string, depth: number, link: string | null) {
        this.token = token
        this.depth = depth
        this.link = link
    }


    static fromJSON({ token, depth, link }): LineageItem {
        let output = new LineageItem(token, depth, link);
        return output
    }


}
