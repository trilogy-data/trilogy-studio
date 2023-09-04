

import { ConceptInterface, Concept } from './Concept';
import { ModelSource } from './ModelSource';

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

export class LocalModel implements ModelInterface {
    name: string;
    concepts: Array<Concept>
    sources: Array<ModelSource>


    constructor(name: string, concepts: Array<Concept>, sources: Array<ModelSource>) {
        this.name = name
        this.concepts = concepts
        this.sources = sources
    }


    static fromJSON({ name, concepts, sources }): Model {
        concepts = concepts.map(dict => {
            return Concept.fromJSON(dict)
        });
        sources = sources.map(dict => {
            return ModelSource.fromJSON(dict)
        });
        let output = new LocalModel(name, concepts, sources);
        return output
    }


}