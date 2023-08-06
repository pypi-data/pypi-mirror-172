import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { INotebookTracker, NotebookPanel, Notebook } from '@jupyterlab/notebook';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { SETTINGS_ID, getTransformerEnabled } from './settings';
import { CellMetadataEditor, IProps as EditorProps } from './widgets/CellMetadataEditor';
import { Cell, isCodeCellModel } from '@jupyterlab/cells';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import TagsUtils from './lib/TagsUtils';
import { IObservableList, IObservableUndoableList } from '@jupyterlab/observables';
import { ICellModel } from '@jupyterlab/cells';
import NotebookUtils from './lib/NotebookUtils';
import { PageConfig } from '@jupyterlab/coreutils';

let transformerSettings: ISettingRegistry.ISettings;
export const TRANSFORMER_NB_FILE_NAME = 'transformer.ipynb'

let transformer_notebook_path: string;
export const getTransformerNotebookDirectory = (): string => {
    return transformer_notebook_path;
}

let editors: EditorProps[] = [];
let isTransformerEnabled: boolean;
const handleNotebookChanged = async (notebookTracker: INotebookTracker, notebookPanel: NotebookPanel) => {
    if (notebookPanel.title.label == TRANSFORMER_NB_FILE_NAME) {
        console.log("Now " + TRANSFORMER_NB_FILE_NAME + "...");
        if(editors.length != notebookPanel.model.cells.length) {
            makeCellTransformerWidgets(notebookPanel);
        }
        notebookPanel.content.activeCellChanged.connect((notebook: Notebook, activeCell: Cell) => {
            let cellElement: HTMLElement = notebook.node.childNodes[notebook.activeCellIndex] as HTMLElement;
            let transformerWidget: HTMLElement = cellElement.querySelector('.cell-transformer-widget') as HTMLElement;
            if(! transformerWidget) {
                const transformerTag = TagsUtils.getCellTransformerTag(notebookPanel, notebook.activeCellIndex);
                let cellId = notebookPanel.model.cells.get(notebook.activeCellIndex).id;
                createCellTransformerWidgets(cellId, notebookPanel, cellElement, transformerTag, isTransformerEnabled);
            }
        });

        notebookPanel.model.cells.changed.connect((cells: IObservableUndoableList<ICellModel>, change: IObservableList.IChangedArgs<ICellModel>) => {
            if(editors.length != notebookPanel.model.cells.length) {
                makeCellTransformerWidgets(notebookPanel);
            }
        });

        const cmd: string = 'import os\n' + 'dir = os.getcwd()';
        let output: any = null;
        try {
            output = await NotebookUtils.sendKernelRequestFromNotebook(notebookPanel, cmd, { result: 'dir' }, true);
            let dir = output.result.data['text/plain'];
            dir = dir.replaceAll("'", "")
            console.log("Transformer notebook directory: " + dir);
            transformer_notebook_path = dir + "/" + TRANSFORMER_NB_FILE_NAME;
        } catch (e) {
            console.warn(e);
            transformer_notebook_path = PageConfig.getOption('serverRoot') + '/' + notebookPanel.context.path;
        }
    }
}

const makeCellTransformerWidgets = (notebookPanel: NotebookPanel) => {
    const cells = notebookPanel.model.cells;
    for (let index = 0; index < cells.length; index++) {
        const isCodeCell = isCodeCellModel(cells.get(index));
        let cellId: string = cells.get(index).id;
        let existedItems = editors.filter(item => item['cellId'] === cellId);
        if(existedItems.length > 0) {
            continue;
        }
        if (! isCodeCell) {
            continue;
        }
        let transformerTag: string = TagsUtils.getCellTransformerTag(notebookPanel, index)? TagsUtils.getCellTransformerTag(notebookPanel, index) : null;

        let cellElement: HTMLElement = notebookPanel.content.node.childNodes[index] as HTMLElement;
        editors[index] = {
            cellId: cellId,
            notebookPanel: notebookPanel,
            transformerTag: transformerTag,
            cellElement: cellElement
        };
        createCellTransformerWidgets(cellId, notebookPanel, cellElement, transformerTag, isTransformerEnabled);
    }
}

const createCellTransformerWidgets = (cellId: string, notebookPanel: NotebookPanel, cellElement: HTMLElement, transformerTag: string, isTransformerEnabled: boolean) => {
    const newChildNode = document.createElement('div')
    newChildNode.className = "cell-transformer-widget";
    let oldWidgets = cellElement.getElementsByClassName("cell-transformer-widget");
    for (let index = 0; index < oldWidgets.length; index++) {
        oldWidgets[index].remove();
    }
    cellElement.insertAdjacentElement('afterbegin', newChildNode);
    ReactDOM.render(
        <CellMetadataEditor
            cellId={cellId}
            notebookPanel={notebookPanel}
            cellElement={cellElement}
            transformerTag={transformerTag}
            transformerSettings={transformerSettings}
            isTransformerEnabled={isTransformerEnabled}
        />,
        newChildNode
    );
}

export default {
    id: 'modeldeploy-proxy-labextension:notebook',
    requires: [ISettingRegistry, INotebookTracker, IDocumentManager],
    autoStart: true,
    activate: async (
        app: JupyterFrontEnd,
        settingRegistry: ISettingRegistry,
        notebookTracker: INotebookTracker,
        docManager: IDocumentManager,
    ) => {
        Promise.all([settingRegistry.load(SETTINGS_ID)]).then(([settings]) => {
            transformerSettings = settings;
            isTransformerEnabled = getTransformerEnabled(settings);
        });

        if(notebookTracker) {
            notebookTracker.currentChanged.connect(handleNotebookChanged);
        }

        app.started.then(() => {
        });

        app.restored.then(async () => {
        });
    },
} as JupyterFrontEndPlugin<void>;
