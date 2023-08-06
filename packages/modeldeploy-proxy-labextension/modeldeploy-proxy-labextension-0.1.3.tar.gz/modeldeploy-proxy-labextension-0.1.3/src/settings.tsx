import { JupyterFrontEnd, JupyterFrontEndPlugin } from '@jupyterlab/application';
import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { JSONObject } from '@lumino/coreutils';

export const SETTINGS_ID = 'modeldeploy-proxy-labextension:settings';
const TRFANFORMER_CONFIG = 'transformerConfig';

export const getTransformerEnabled = (settings: ISettingRegistry.ISettings): boolean => {
    try {
        let transformerSettings = settings.get(TRFANFORMER_CONFIG).composite as JSONObject;
        if(typeof transformerSettings.enabled === 'string' && transformerSettings.enabled === 'true') {
            return true;
        } else if(typeof transformerSettings.enabled === 'boolean') {
            return transformerSettings.enabled
        }
    } catch (error) {
        console.error(error);
    }
    return false;
};

export const setTransformerEnabled = (settings: ISettingRegistry.ISettings, enabled: boolean) => {
    let config : IConfig = {
        enabled: enabled
    }
    settings.set(TRFANFORMER_CONFIG, config as unknown as JSONObject).catch((reason: Error) => {
        console.error('Failed to set transformer config: ' + reason.message);
    });
};

interface IConfig {
    enabled: boolean;
}

const defaultConfig: IConfig = {
    enabled: false
}

export default {
    id: SETTINGS_ID,
    requires: [ ISettingRegistry ],
    autoStart: true,
    activate: (
        app: JupyterFrontEnd,
        settingRegistry: ISettingRegistry
    ): void => {
        Promise.all([settingRegistry.load(SETTINGS_ID)]).then(([settings]) => {
            try {
                settings.get(TRFANFORMER_CONFIG).composite as JSONObject;
            } catch (error) {
                settingRegistry.set(SETTINGS_ID, TRFANFORMER_CONFIG, defaultConfig as unknown as JSONObject).catch((reason: Error) => {
                    console.error('Failed to set transformer config: ' + reason.message);
                });
            }
        });
    },
} as JupyterFrontEndPlugin<void>;
