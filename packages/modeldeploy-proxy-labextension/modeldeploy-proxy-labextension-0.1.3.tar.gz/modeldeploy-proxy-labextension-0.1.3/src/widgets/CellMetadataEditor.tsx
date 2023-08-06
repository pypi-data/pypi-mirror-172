import * as React from 'react';
import CloseIcon from '@material-ui/icons/Close';
import CheckIcon from '@material-ui/icons/Check';
import { IconButton } from '@material-ui/core';
import { Select } from './../components/Select';
import TagsUtils from './../lib/TagsUtils';
import { NotebookPanel } from '@jupyterlab/notebook';
import { Chip, Tooltip } from '@material-ui/core';
import { CellMetadataEditorDialog } from './CellMetadataEditorDialog';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { getTransformerEnabled } from './../settings';
import { fetchTransformerStattes, issueTransformerStatesChange, addStatesChangeListener, ITransformerStates } from './../states'

const CELL_TYPE_NA = 'na';
const CELL_TYPE_NA_LABEL = '-';

export const CELL_TYPE_PREPROCESSOR = 'preprocessor';
export const CELL_TYPE_POSTPROCESSOR = 'postprocessor';
export const CELL_TYPE_REQUIREMENTS = 'requirements';
const CELL_TYPES: any[] = [
    {
        value: CELL_TYPE_NA,
        label: CELL_TYPE_NA_LABEL,
        helpText: null,
        chipColor: null 
    },
    {
        value: CELL_TYPE_REQUIREMENTS,
        label: 'Requirements',
        helpText: 'The code in this cell will be parsed as requirements packages and install in system.',
        chipColor: 'a32626'
    },
    {
        value: CELL_TYPE_PREPROCESSOR,
        label: 'Pre processor',
        helpText: 'The code in this cell will be parsed as preprocessor for the predict function of deployed model.',
        chipColor: 'ee7a1a'
    },
    {
        value: CELL_TYPE_POSTPROCESSOR,
        label: 'Post processor',
        helpText: 'The code in this cell will be parsed as postprocessor for the predict function of deployed model.',
        chipColor: '773d0d'
    },
    {
        value: 'functions',
        label: 'Extra functions',
        helpText: 'The code in this cell will be parsed as referenced function for the preprocessor or postprocessor.',
        chipColor: 'a32626'
    }
];

const CELL_TYPE_SELECT_OPTIONS = CELL_TYPES
    //.filter(item => item['value'] !== CELL_TYPE_NA)
    .map(item => {
        const newItem = { ...item };
        delete newItem['helpText'];
        delete newItem.chipColor;
        return newItem;
    });

export const RESERVED_CELL_NAMES: string[] = CELL_TYPES
    .filter(item => item['value'] !== CELL_TYPE_NA)
    .map(item => {
        return item['value'];
    });

export const RESERVED_CELL_NAMES_HELP_TEXT = CELL_TYPES
    .reduce((obj, item) => {
        obj[item.value] = item.helpText;
        return obj;
    } ,{});

export const RESERVED_CELL_NAMES_CHIP_COLOR = CELL_TYPES
    .reduce((obj, item) => {
        obj[item.value] = item.chipColor;
        return obj;
    } ,{});

export interface IProps {
    notebookPanel: NotebookPanel;
    cellElement: any;
    transformerTag?: string;
    transformerSettings?: ISettingRegistry.ISettings;
    isTransformerEnabled?: boolean;
    cellId?: string;
}

interface IState {
    transformerTag?: string;
    isChipVisible?: boolean;
    isSelectorVisible?: boolean;
    cellMetadataEditorDialog?: boolean;
    dialogTitle?: string;
    dialogContent?: string;
    isTransformerEnabled: boolean;
    typeSelectOptions: any[];
}

export class CellMetadataEditor extends React.Component<IProps, IState> {
    transformerStates: ITransformerStates = null;

    constructor(props: IProps) {
        super(props);
        this.transformerStates = fetchTransformerStattes();
        this.updateLocalTransformerStates(props.transformerTag, true);
        addStatesChangeListener(this.onStatesChangeCallback);
        issueTransformerStatesChange(this.props.cellId, this.transformerStates);
        const defaultState: IState = {
            transformerTag: props.transformerTag?props.transformerTag : CELL_TYPE_NA,
            isChipVisible: RESERVED_CELL_NAMES.includes(props.transformerTag)? true: false,
            isSelectorVisible: false,
            cellMetadataEditorDialog: false,
            dialogTitle: 'Warning',
            dialogContent: '',
            isTransformerEnabled: this.props.isTransformerEnabled,
            typeSelectOptions: this.getTypeSelectOptions([props.transformerTag])
        };
        this.state = defaultState;
        this.updateCurrentCellTag = this.updateCurrentCellTag.bind(this);
        this.toggleTagsEditorDialog = this.toggleTagsEditorDialog.bind(this);
        if(this.props.transformerSettings) {
            this.props.transformerSettings.changed.connect(this.updateTransformerEnabled);
        }
    }

    isTagged = (tag: string): boolean => {
        if(tag === CELL_TYPE_PREPROCESSOR) {
            return this.transformerStates.isPreprocessorTagged;
        } else if(tag === CELL_TYPE_POSTPROCESSOR) {
            return this.transformerStates.isPostprocessorTagged;
        } else if(tag === CELL_TYPE_REQUIREMENTS) {
            return this.transformerStates.isRequirementsTagged;
        }
        return false;
    }

    updateLocalTransformerStates = (tag: string, tagged: boolean): void => {
        if(tag === CELL_TYPE_PREPROCESSOR) {
            this.transformerStates.isPreprocessorTagged = tagged;
        } else if(tag === CELL_TYPE_POSTPROCESSOR) {
            this.transformerStates.isPostprocessorTagged = tagged;
        } else if(tag === CELL_TYPE_REQUIREMENTS) {
            this.transformerStates.isRequirementsTagged = tagged;
        }
    }

    onStatesChangeCallback = (issuer: string, newStates: ITransformerStates) : void => {
        if(issuer == this.props.cellId) {
            return;
        };
        this.transformerStates = newStates;
        this.setState({typeSelectOptions: this.getTypeSelectOptions([this.state.transformerTag])});
    }

    updateTransformerEnabled = (settings: ISettingRegistry.ISettings): void => {
        this.setState({isTransformerEnabled: getTransformerEnabled(settings)});
    };

    updateCurrentCellTag = (value: string) => {
        if(value !== this.state.transformerTag) {
            this.updateLocalTransformerStates(this.state.transformerTag, false);
            this.updateLocalTransformerStates(value, true);
            issueTransformerStatesChange(this.props.cellId, this.transformerStates);
            if (RESERVED_CELL_NAMES.includes(value)) {
                this.setState({ transformerTag: value });
            } else if(CELL_TYPE_NA === value) {
                this.setState({ transformerTag: CELL_TYPE_NA });
            }
        }
    };

    saveCellTagInNotebookFile = () => {
        let value = this.state.transformerTag;
        let isDuplicated = false;
        if(value == CELL_TYPE_PREPROCESSOR || value == CELL_TYPE_POSTPROCESSOR || value == CELL_TYPE_REQUIREMENTS) {
            isDuplicated = TagsUtils.isTransformerTagExistedInOtherCells(
                this.props.notebookPanel,
                this.props.notebookPanel.content.activeCellIndex,
                value
            );
        }

        if(isDuplicated) {
            this.setState({ dialogContent: value + " is limited to be just one." });
            this.toggleTagsEditorDialog();
        } else {
            if (RESERVED_CELL_NAMES.includes(value)) {
                let cellMetadata = {
                    transformerTag: value,
                };
                TagsUtils.setCellTransformerTag(
                    this.props.notebookPanel,
                    this.props.notebookPanel.content.activeCellIndex,
                    cellMetadata
                ).then(newValue => {
                    this.hideSelector();
                });
            } else if(CELL_TYPE_NA === value) {
                TagsUtils.resetCellTransformerTag(
                    this.props.notebookPanel,
                    this.props.notebookPanel.content.activeCellIndex,
                ).then(newValue => {
                    this.hideSelector();
                });
            }
        }
    }

    removeCellTagInNotebookFile = () => {
        TagsUtils.resetCellTransformerTag(
            this.props.notebookPanel,
            this.props.notebookPanel.content.activeCellIndex,
        ).then(newValue => {
            // update transformerTag state HERE to avoid a tricky issue
            this.setState({ transformerTag: CELL_TYPE_NA });
            this.hideSelector();
        });
    }

    isEqual(a: any, b: any): boolean {
        return JSON.stringify(a) === JSON.stringify(b);
    }

    componentDidUpdate(prevProps: Readonly<IProps>, prevState: Readonly<IState>) {
        this.hideEditorIfNotCodeCell();
    }

    hideEditorIfNotCodeCell() {
    }

    static getDerivedStateFromProps (props: IProps, state: IState) : any {
        return null;
    }

    onBeforeUpdate = (value: string) => {
        if (value === this.props.transformerTag) {
            return false;
        }
        return false;
    };

    toggleSelector() {
        if(this.state.isSelectorVisible) {
            this.hideSelector();
        } else {
            this.showSelector();
        }
    }

    showSelector() {
        this.setState({
            isSelectorVisible: true,
            isChipVisible: false
        });
    }

    hideSelector() {
        this.setState({
            isSelectorVisible: false,
            isChipVisible: RESERVED_CELL_NAMES.includes(this.state.transformerTag)? true : false
        });
    }

    onChipClick() {
        this.setState({ isSelectorVisible: true, isChipVisible: false });
    }

    toggleTagsEditorDialog() {
        this.setState({ cellMetadataEditorDialog: !this.state.cellMetadataEditorDialog });
    }

    componentDidMount = () => {
    };

    getTypeSelectOptions = (keepTags: string[]): any[] => {
        return CELL_TYPE_SELECT_OPTIONS
        .filter(item => (keepTags.includes(item['value']) || !this.isTagged(item['value'])))
        .map(item => {
            const newItem = { ...item };
            delete newItem['helpText'];
            delete newItem.chipColor;
            return newItem;
        });
    }

    render() {
        const cellType = RESERVED_CELL_NAMES.includes(this.state.transformerTag)? this.state.transformerTag : 'na';
        const cellColor = 'transparent';

        // add class names for styling
        if(! this.state.isTransformerEnabled) {
            this.props.cellElement.classList.remove('with-transformer-editor');
            this.props.cellElement.classList.remove('with-transformer-chip');
        } else if(this.state.isSelectorVisible) {
            this.props.cellElement.classList.add('with-transformer-editor');
            this.props.cellElement.classList.remove('with-transformer-chip');
        } else if(this.state.isChipVisible) {
            this.props.cellElement.classList.remove('with-transformer-editor');
            this.props.cellElement.classList.add('with-transformer-chip');
        } else {
            this.props.cellElement.classList.remove('with-transformer-editor');
            this.props.cellElement.classList.remove('with-transformer-chip');
        }

        return (
            <React.Fragment>
                <div className={ 'transformer-inline-cell-metadata' + ((this.state.isTransformerEnabled && this.state.isChipVisible)? '' : ' hidden') }>
                    <Tooltip
                        placement="top"
                        key={this.state.transformerTag + 'tooltip'}
                        title={
                            RESERVED_CELL_NAMES.includes(this.state.transformerTag)?
                            RESERVED_CELL_NAMES_HELP_TEXT[this.state.transformerTag] :
                            'This cell starts the pipeline step: ' + this.state.transformerTag
                        }
                    >
                        <Chip
                            className={ 'transformer-meta-chip' }
                            key={ this.state.transformerTag }
                            label={ this.state.transformerTag }
                            onClick={() => this.onChipClick()}
                        />
                    </Tooltip>
                </div>
                <div className={ 'transformer-metadata-editor-wrapper' + ((this.state.isTransformerEnabled && this.state.isSelectorVisible)? '' : ' hidden') }>
                    <div
                        className={ 'transformer-cell-metadata-editor' }
                        style={{ borderLeft: `2px solid ${cellColor}` }}
                    >
                        <Select
                            updateValue={this.updateCurrentCellTag}
                            values={this.state.typeSelectOptions}
                            value={cellType}
                            label={'Cell type'}
                            index={0}
                            variant="outlined"
                            style={{ width: 'auto', minWidth: '14em' }}
                        />
                        <IconButton
                            aria-label="remove"
                            onClick={() => this.removeCellTagInNotebookFile()}
                        >
                            <CloseIcon fontSize="small" />
                        </IconButton>
                        <IconButton
                            aria-label="apply"
                            onClick={() => this.saveCellTagInNotebookFile()}
                        >
                            <CheckIcon fontSize="small" />
                        </IconButton>
                        <IconButton
                            className={ 'transformer-cell-metadata-editor-toggle' }
                            aria-label="toggle"
                            onClick={() => this.toggleSelector()}
                            style={{ width: '0', height: '0', padding: '0' }}
                        />
                    </div>
                    <div className={ 'transformer-cell-metadata-editor-helper-text' + (this.state.isSelectorVisible ? '' : ' hidden') }>
                    </div>
                </div>
                <CellMetadataEditorDialog
                    open={this.state.cellMetadataEditorDialog}
                    toggleDialog={this.toggleTagsEditorDialog}
                    title={this.state.dialogTitle}
                    dialogContent={this.state.dialogContent}
                />
            </React.Fragment>
        );
    }
}
