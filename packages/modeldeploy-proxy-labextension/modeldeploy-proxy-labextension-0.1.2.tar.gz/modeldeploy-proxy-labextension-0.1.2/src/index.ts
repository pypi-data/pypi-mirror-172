import { JupyterFrontEndPlugin } from '@jupyterlab/application';
import TransformerCellSidebarPlugin from './sidebar';
import TransformerLeftPanelPlugin from './leftpanel';
//import StateDBPlugin from './statedb';
import SettingsPlugin from './settings';
import NotebookPlugin from './notebook';

export default [ TransformerCellSidebarPlugin, TransformerLeftPanelPlugin, SettingsPlugin, NotebookPlugin ] as JupyterFrontEndPlugin<any>[];
