import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { Token } from '@lumino/coreutils';
import { StateDB, IStateDB } from '@jupyterlab/statedb';

const id = 'transformer-extension:ITransformerState';
const ITransformerState = new Token<ITransformerState>(id);
interface ITransformerState {}
class TransformerState implements ITransformerState {}

export default {
    id: 'modeldeploy-proxy-labextension:statedb',
    requires: [ IStateDB ],
    provides: ITransformerState,
    autoStart: true,
    activate: (
        app: JupyterFrontEnd,
        state: IStateDB
    ): ITransformerState => {
        const transformerState = new TransformerState();
        const new_state = new StateDB();

        app.started.then(() => {
            //new_state.save(id, { 'gg': true });
        });

        app.restored.then(async () => {
            const value = await new_state.fetch(id);
            console.log(value);
        });

        return transformerState;
    },
} as JupyterFrontEndPlugin<ITransformerState>;
