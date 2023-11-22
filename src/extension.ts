// // The module 'vscode' contains the VS Code extensibility API
// // Import the module and reference it with the alias vscode in your code below
// import * as vscode from 'vscode';

// // This method is called when your extension is activated
// // Your extension is activated the very first time the command is executed
// export function activate(context: vscode.ExtensionContext) {

// 	// Use the console to output diagnostic information (console.log) and errors (console.error)
// 	// This line of code will only be executed once when your extension is activated
// 	console.log('Congratulations, your extension "codecompletion88" is now active!');

// 	// The command has been defined in the package.json file
// 	// Now provide the implementation of the command with registerCommand
// 	// The commandId parameter must match the command field in package.json
// 	let disposable = vscode.commands.registerCommand('codecompletion88.helloWorld', () => {
// 		// The code you place here will be executed every time your command is executed
// 		// Display a message box to the user
// 		vscode.window.showInformationMessage('Hello VS Code from CodeCompletion!');
// 	});



// 	context.subscriptions.push(disposable);
// }

// // This method is called when your extension is deactivated
// export function deactivate() {}

import * as vscode from 'vscode';

/** Supported language type */
const LANGUAGES = ['typescriptreact', 'typescript', 'javascript', 'javascriptreact'];

const dictionary = ['hello', 'nihao', 'dajiahao', 'leihaoa'];

/** Commands that are triggered after the user chooses items */
const COMMAND_NAME = 'my_code_completion_choose_item';

/** The command triggered when the recommended item is registered */
function registerCommand(command: string) {
    vscode.commands.registerTextEditorCommand(
        command,
        (editor, edit, ...args) => {
            const [text] = args;
            // TODO records the current content in the dictionary and automatically updates the dictionary.
        }
    );
}

export function activate(context: vscode.ExtensionContext) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "codecompletion88" is now active!');

	// The command has been defined in the package.json
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('codecompletion88.helloWorld', () => {
		// The code you place here will be executed every time your command is executed
		// Display a message box to the user
		vscode.window.showInformationMessage('Hello VS Code from CodeCompletion!');
	});
    // /** Trigger a list of recommended characters */
    // const triggers = [' '];
    // const completionProvider = vscode.languages.registerCompletionItemProvider(LANGUAGES, {
    //     async provideCompletionItems(document: vscode.TextDocument, position: vscode.Position, token: vscode.CancellationToken, context: vscode.CompletionContext) {
    //         const completionItem: vscode.CompletionItem = {
    //             label: 'Hello VsCode',
    //         };
    //         return [completionItem];
    //     }
    // }, ...triggers);

    // context.subscriptions.push(completionProvider);

    // /** Trigger a list of recommended characters */
    // const triggers = [' '];
    // const completionProvider = vscode.languages.registerCompletionItemProvider(LANGUAGES, {
    //     async provideCompletionItems(document: vscode.TextDocument, position: vscode.Position, token: vscode.CancellationToken, context: vscode.CompletionContext) {
    //         const range = new vscode.Range(new vscode.Position(position.line, 0), position);
    //         const text = document.getText(range);

    //         const completionItemList: vscode.CompletionItem[] = dictionary.filter(item => item.startsWith(text)).map((item, idx) => ({
    //             label: item,
    //             preselect: idx === 0,
    //             documentation: 'My dedicated VsCode plug-ins provider',
    //             sortText: `my_completion_${idx}`,
    //         }));
    //         return completionItemList;
    //     }
    // }, ...triggers);


    /** Trigger a list of recommended characters */
    const triggers = [' '];
    registerCommand(COMMAND_NAME);
    const completionProvider = vscode.languages.registerCompletionItemProvider(LANGUAGES, {
        async provideCompletionItems(document: vscode.TextDocument, position: vscode.Position, token: vscode.CancellationToken, context: vscode.CompletionContext) {
            const range = new vscode.Range(new vscode.Position(position.line, 0), position);
            const text = document.getText(range);
            const completionItemList: vscode.CompletionItem[] = dictionary.filter(item => item.startsWith(text)).map((item, idx) => ({
                label: item,
                preselect: idx === 0,
                documentation: 'My dedicated VsCode plug-ins provider',
                sortText: `my_completion_${idx}`,
                command: {
                    arguments: [text],
                    command: COMMAND_NAME,
                    title: 'choose item'
                },
            }));
            return completionItemList;
        }
    }, ...triggers);

    context.subscriptions.push(completionProvider);



    context.subscriptions.push(disposable);
}

// This method is called when your extension is deactivated
export function deactivate() {}