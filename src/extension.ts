import * as vscode from 'vscode';
import { execSync } from 'child_process';
import * as path from 'path';

/** Supported language type */
const LANGUAGES = ['typescriptreact', 'typescript', 'javascript', 'javascriptreact'];

let dictionary = ['hello', 'nihao', 'dajiahao', 'leihaoa'];

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
function callPythonScript(name: string): string {
    const rootDirectory = path.resolve(__dirname, '..');
    const srcDirectory = path.join(rootDirectory, 'src');
    const pythonScriptPath = path.join(srcDirectory, 'BMNCCS.py');

    // Create a virtual environment
    const venvDirectory = path.join(srcDirectory, 'env');
    // execSync(`python -m venv "${venvDirectory}"`);

    // Activate the virtual environment
    const activateDirectory = path.join(venvDirectory, 'bin', 'activate');  // Adjust for Unix/MacOS
    const activateCommand = `source "${activateDirectory}"`;
    execSync(activateCommand, { shell: '/bin/zsh' }); // Use '/bin/zsh' for macOS

    // Install NumPy in the virtual environment
    // execSync('python3 -m pip install -U mypy javalang ast numpy');
    // execSync('python3 -m pip install --upgrade pip');
    // console.log('Installing packages...');
    // execSync('python3 -m pip install -U mypy');
    // execSync('python3 -m pip install -U javalang');
    // // execSync('python3 -m pip install -U ast');
    // execSync('python3 -m pip install -U numpy');

    console.log('Running python script...');
    const resultBuffer = execSync(`python3 "${pythonScriptPath}" "${name}"`, { encoding: 'utf-8' });
    return resultBuffer.trim();
}

function replaceVariableName(methodString: string, variableName: string): string {
    // Using a regular expression to replace 'HelloWorld' with the provided variable name
    const replacedString = methodString.replace(/HelloWorld/g, variableName);
    return replacedString;
}

function replaceVariableNameInArray(localVariableName: string, inputString: string): string[] {
    try {
        // Removing square brackets and single quotes from the string
        const cleanedString = inputString.replace(/[\[\]']+/g, '');

        // Splitting the cleaned string into an array using ', ' as the separator
        const resultArray = cleanedString.split(', ');

        // Replace 'HelloWorld' with the provided local variable name in each array element
        const modifiedArray = resultArray.map(item => replaceVariableName(item, localVariableName));

        return modifiedArray;
    } catch (error) {
        console.error('Error converting string to array:', error);
        return [];
    }
}



export function activate(context: vscode.ExtensionContext) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('Congratulations, your extension "codecompletion88" is now active!');

    //TODO: get the local vairaible name
    const recommendationString = callPythonScript('hello');
    console.log(recommendationString);
    const recommendtaions = replaceVariableNameInArray("display", recommendationString);
    console.log(recommendtaions);
    dictionary = recommendtaions;
	// The command has been defined in the package.json
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let disposable = vscode.commands.registerCommand('codecompletion88.helloWorld', () => {
		// The code you place here will be executed every time your command is executed
		// Display a message box to the user
		vscode.window.showInformationMessage('Hello VS Code from CodeCompletion88!');
	});

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