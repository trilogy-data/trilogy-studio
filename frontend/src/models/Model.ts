

import { ConceptInterface, Concept } from './Concept';

export interface ModelInterface {
    name: string;
    concepts: Array<ConceptInterface>
}




export class Model implements ModelInterface {
    name: string;
    concepts: Array<Concept>


    constructor(name: string, concepts: Array<Concept>) {
        this.name = name
        this.concepts = concepts
    }


    static fromJSON({ name, concepts }): Model {
        concepts = concepts.map(dict => {
            return Concept.fromJSON(dict)
        });
        let output = new Model(name, concepts);
        return output
    }


}
