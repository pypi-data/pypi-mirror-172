import * as React from 'react';
import { Button, Dialog, DialogActions, DialogContent, DialogTitle, Grid } from '@material-ui/core';

interface ICellMetadataEditorDialog {
    open: boolean;
    title: string;
    dialogContent: string;
    toggleDialog: Function;
}

export const CellMetadataEditorDialog: React.FunctionComponent<ICellMetadataEditorDialog> = props => {
    const handleClose = () => {
        props.toggleDialog();
    };

    return (
        <Dialog
            open={props.open}
            onClose={handleClose}
            fullWidth={true}
            maxWidth={'sm'}
            scroll="paper"
            aria-labelledby="scroll-dialog-title"
            aria-describedby="scroll-dialog-description"
        >
            <DialogTitle id="scroll-dialog-title">
                <p className={'dialog-title'} >{props.title}</p>
            </DialogTitle>
            <DialogContent dividers={true} style={{ paddingTop: 0 }}>
                <Grid container direction="column" justify="center" alignItems="center">
                    <Grid
                        container
                        direction="row"
                        justify="space-between"
                        alignItems="center"
                        style={{ marginTop: '15px' }}
                    >
                        <p>{props.dialogContent}</p>
                    </Grid>
                </Grid>
            </DialogContent>
            <DialogActions>
                <Button onClick={handleClose} color="primary">Ok</Button>
            </DialogActions>
    </Dialog>
  );
};
