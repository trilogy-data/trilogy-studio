
import { LineageItemInterface, LineageItem } from "./LineageItem";

export interface ConceptInterface {
    key: string,
    name: string,
    namespace: string,
    datatype: string,
    purpose: string,
    description: string | null,
    lineage: Array<LineageItemInterface>
}

export class Concept implements ConceptInterface {
    key: string
    name: string
    namespace: string
    datatype: string
    purpose: string
    description: string | null
    lineage: Array<LineageItem>


    constructor(name: string, key:string, namespace: string, datatype: string, purpose: string, 
        description: string | null, lineage: Array<LineageItem>) {
        this.name = name
        this.key = key
        this.namespace = namespace
        this.datatype = datatype
        this.purpose = purpose
        this.description = description
        this.lineage = lineage
    }


    static fromJSON({ key, name, namespace, datatype, purpose, description, lineage }):Concept {
        lineage = lineage.map(dict => {
            return LineageItem.fromJSON(dict)
        });
        let output = new Concept(name, key, namespace, datatype, purpose, description, lineage);
        return output
    }


}