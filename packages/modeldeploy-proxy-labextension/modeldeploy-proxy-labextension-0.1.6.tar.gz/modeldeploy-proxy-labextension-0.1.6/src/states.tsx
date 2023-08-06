import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { Token } from '@lumino/coreutils';

const id = 'transformer-extension:ITransformerStates';
const ITransformerStates = new Token<ITransformerStates>(id);
export interface ITransformerStates {
    isPreprocessorTagged?: boolean;
    isPostprocessorTagged?: boolean;
    isRequirementsTagged?: boolean;
}
const transformerStates: ITransformerStates = {
    isPreprocessorTagged: false,
    isPostprocessorTagged: false,
    isRequirementsTagged: false
}
let stateChangeListeners: ((trigger: string, newStates: ITransformerStates) => void)[] = [];

export const fetchTransformerStattes = (): ITransformerStates => {
    return transformerStates;
}

export const issueTransformerStatesChange = (issuer: string, states: ITransformerStates): void => {
    Object.assign(transformerStates, states)
    stateChangeListeners.forEach(callback => {
        callback(issuer, transformerStates);
    });
}

export const addStatesChangeListener = (callback: (trigger: string, newStates: ITransformerStates) => void): void => {
    stateChangeListeners.push(callback);
}

export default {
    id: 'modeldeploy-proxy-labextension:states',
    provides: ITransformerStates,
    autoStart: true,
    activate: (
        app: JupyterFrontEnd,
    ): ITransformerStates => {
        app.started.then(() => {
        });

        app.restored.then(async () => {
        });

        return transformerStates;
    },
} as JupyterFrontEndPlugin<ITransformerStates>;
