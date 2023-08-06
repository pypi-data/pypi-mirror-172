import * as React from 'react';
import { ThemeProvider } from '@material-ui/core/styles';
import { theme } from './../theme';
import { Button } from '@material-ui/core';
import { executeRpc, globalUnhandledRejection } from './../lib/RPCUtils';
import NotebookUtils from './../lib/NotebookUtils';
import { Kernel } from '@jupyterlab/services';
import { Switch } from '@material-ui/core';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { getTransformerEnabled, setTransformerEnabled } from './../settings';
import { getTransformerNotebookDirectory } from './../notebook';

interface IProps {
    transformerSettings: ISettingRegistry.ISettings
}

interface IState {
    isEnabled: boolean;
}

export class TransformerLeftPanel extends React.Component<IProps, IState> {
    constructor(props: IProps) {
        super(props);
        const defaultState: IState = {
            isEnabled: getTransformerEnabled(this.props.transformerSettings)
        };
        this.state = defaultState;
    }

    componentDidMount = () => {
        // Notebook tracker will signal when a notebook is changed
        console.log("transformerEnabled = " + getTransformerEnabled(this.props.transformerSettings));
    };

    componentDidUpdate = (
        prevProps: Readonly<IProps>,
        prevState: Readonly<IState>,
    ) => {
        console.log("componentDidUpdate");
    };

    applyTransformerToProxy = async () => {
        console.log('applyTransformerToProxy');

        try {
            const kernel: Kernel.IKernelConnection = await NotebookUtils.createNewKernel();
            await executeRpc(kernel, 'log.setup_logging');
            const args = {
                source_notebook_path: getTransformerNotebookDirectory()
            }
            const result = await executeRpc(kernel, 'nb.parse_notebook', args);
            console.log(result);
        } catch (error) {
            globalUnhandledRejection({ reason: error });
            throw error;
        }
    };

    onTransformerEnableChanged = (enabled: boolean) => {
        this.setState({ isEnabled: enabled });
        setTransformerEnabled(this.props.transformerSettings, enabled);
    };

    render() {
        return (
            <ThemeProvider theme={theme}>
                <div className={'leftpanel-transformer-widget'} key="transformer-widget" style={{padding: 'var(--jp-code-padding)'}}>
                    <div className={'leftpanel-transformer-widget-content'}>
                        <div className="transformer-header" style={{fontSize: 'var(--jp-ui-font-size3)'}} >
                            <p>Transformer Panel</p>
                        </div>

                        <div className='transformer-component' >
                            <div>
                                <p className="transformer-header" style={{ color: theme.transformer.headers.main, fontSize: 'var(--jp-ui-font-size1)'}}>
                                    Transformer is the extension for model inference, it injects pre and post preocessors defined in <strong style={{fontSize: 'var(--jp-ui-font-size2)'}}>transformer.ipynb</strong> notebook.
                                </p>
                            </div>
                        </div>

                        <div className="transformer-toggler">
                            <React.Fragment>
                                <div className="toolbar input-container">
                                    <Switch
                                        checked={this.state.isEnabled}
                                        onChange={c => this.onTransformerEnableChanged(c.target.checked)}
                                        color="primary"
                                        name="enable-transformer"
                                        inputProps={{ 'aria-label': 'primary checkbox' }}
                                        classes={{ root: 'material-switch' }}
                                    />
                                    <div className={'switch-label'} style={{ display: 'inline-block' }}>
                                        {(this.state.isEnabled ? 'Disable' : 'Enable') + ' transformer widgets'}
                                    </div>
                                </div>
                            </React.Fragment>
                        </div>

                        <div className={ 'transformer-component ' + (this.state.isEnabled ? '' : 'hidden') } >
                            <div className="input-container add-button">
                                <Button
                                    variant="contained"
                                    color="primary"
                                    size="small"
                                    title="Apply the changes."
                                    onClick={this.applyTransformerToProxy}
                                    disabled={ false }
                                    style={{ marginLeft: '10px', marginTop: '0px' }}
                                >
                                    Apply Changes
                                </Button>
                            </div>
                        </div>
                    </div>
                </div>
            </ThemeProvider>
        );
    }
}
