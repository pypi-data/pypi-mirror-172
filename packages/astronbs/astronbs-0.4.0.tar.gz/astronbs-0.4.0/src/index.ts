import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { IDocumentManager } from '@jupyterlab/docmanager';
import { ILauncher } from '@jupyterlab/launcher';
import { imageIcon } from '@jupyterlab/ui-components';

import { requestAPI } from './handler';

/**
 * Initialization data for the astronbs extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'astronbs:plugin',
  autoStart: true,
  optional: [ISettingRegistry, ILauncher, IFileBrowserFactory, IDocumentManager],
  activate: (
    app: JupyterFrontEnd, 
    settingRegistry: ISettingRegistry | null,
    launcher: ILauncher | null,
    fileBrowser: IFileBrowserFactory,
    docManager: IDocumentManager | null
  ) => {
    console.log('JupyterLab extension astronbs is activated!');

    if (settingRegistry) {
      settingRegistry
        .load(plugin.id)
        .then(settings => {
          console.log('astronbs settings loaded:', settings.composite);
        })
        .catch(reason => {
          console.error('Failed to load settings for astronbs.', reason);
        });
    }

    app.commands.addCommand('astronbs:reduction_template', {
      // code to run when this command is executed
      execute: () => {
        const reply = requestAPI<any>(
          'reduction_template', 
          {
            body: JSON.stringify(
                      {
                        'path': fileBrowser.defaultBrowser.model.path,
                        'package_path': 'astronbs.notebooks',
                        'nb_name': 'reduction_template.ipynb'
                    }),
            method: 'POST'
          }
        );
        console.log(reply)
        reply.then(data => {
          console.log(data);
          if (docManager) {
            docManager.open(data['path']);
          }
        });
      },
      icon: imageIcon,
      label: 'Reduction Template'
    });
    app.commands.addCommand('astronbs:reprojection_template', {
      // code to run when this command is executed
      execute: () => {
       const reply = requestAPI<any>(
          'reprojection_template', 
          {
            body: JSON.stringify({'path': fileBrowser.defaultBrowser.model.path}), 
            method: 'POST'
          }
        );
        console.log(reply)
        reply.then(data => {
          console.log(data);
          if (docManager) {
            docManager.open(data['path']);
          }
        });
      },
      icon: imageIcon,
      label: 'Reprojection Template'
    });

    app.commands.addCommand('astronbs:light_combo_template', {
      // code to run when this command is executed
      execute: () => {
        const reply = requestAPI<any>(
          'light_combo_template',
          {
            body: JSON.stringify({'path': fileBrowser.defaultBrowser.model.path}),
            method: 'POST'
          }
        );
        console.log("I am back in open2");
        console.log(reply)
        reply.then(data => {
          console.log(data);
          if (docManager) {
            docManager.open(data['path']);
          }
        });
      },
      icon: imageIcon,
      label: 'Light Combo Template'
    });
    app.commands.addCommand('astronbs:01_seeing_profile', {
      // code to run when this command is executed
      execute: () => {
        const reply = requestAPI<any>(
          'nb_make',
          {
            body: JSON.stringify(
                      {
                        'path': fileBrowser.defaultBrowser.model.path,
                        'package_path': 'stellarphot.notebooks.photometry',
                        'nb_name': '01-viewer-seeing-template.ipynb'
                    }),
            method: 'POST'
          }
        );
        console.log(reply)
        reply.then(data => {
          console.log(data);
          if (docManager) {
            docManager.open(data['path']);
          }
        });
      },
      icon: imageIcon,
      label: '01 Seeing Profile'
    });

    app.commands.addCommand('astronbs:02_comp_stars', {
      // code to run when this command is executed
      execute: () => {
        const reply = requestAPI<any>(
          'nb_make',
          {
            body: JSON.stringify(
                      {
                        'path': fileBrowser.defaultBrowser.model.path,
                        'package_path': 'stellarphot.notebooks.photometry',
                        'nb_name': '02-comp-star-plotter-template.ipynb'
                    }),
            method: 'POST'
          }
        );
        console.log(reply)
        reply.then(data => {
          console.log(data);
          if (docManager) {
            docManager.open(data['path']);
          }
        });
      },
      icon: imageIcon,
      label: '02 Comparison Stars'
    });

    // Add item to launcher
    if (launcher) {
      launcher.add({
        command: 'astronbs:reduction_template',
        category: 'Astro',
        rank: 0
      });
      
      launcher.add({
        command: 'astronbs:reprojection_template',
        category: 'Astro',
        rank: 10
      });

      launcher.add({
        command: 'astronbs:light_combo_template',
        category: 'Astro',
        rank: 20
      });
      launcher.add({
        command: 'astronbs:01_seeing_profile',
        category: 'Photometry',
        rank: 0
      });
      launcher.add({
        command: 'astronbs:02_comp_stars',
        category: 'Photometry',
        rank: 0
      });
    }

    requestAPI<any>('get_example')
      .then(data => {
        console.log(data);
      })
      .catch(reason => {
        console.error(
          `The astronbs server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
