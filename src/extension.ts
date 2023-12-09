import * as vscode from 'vscode';
import { execSync } from 'child_process';
import * as path from 'path';
import { get } from 'http';

/** Supported language type */
// const LANGUAGES = ['typescriptreact', 'typescript', 'javascript', 'javascriptreact'];
const LANGUAGES = ['java'];

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

function initCCSController(mode: string) {
    console.log('Initiating CCSController...');
    const rootDirectory = path.resolve(__dirname, '..');
    const srcDirectory = path.join(rootDirectory, 'src');
    const pythonScriptPath = path.join(srcDirectory, 'CCSController.py');

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

    
    // const resultBuffer = execSync(`python3 "${pythonScriptPath}" "${mode}"`, { encoding: 'utf-8' });
    // return resultBuffer.trim();
}


function callCCSController(mode: string, context_file_path: string, lineNum: number, line: string): string {
    const rootDirectory = path.resolve(__dirname, '..');
    const srcDirectory = path.join(rootDirectory, 'src');
    const pythonScriptPath = path.join(srcDirectory, 'CCSController.py');

    console.log('Sending context to CCSController...');
    const resultBuffer = execSync(`python3 "${pythonScriptPath}" "${mode}" "${context_file_path}" "${lineNum}" "${line}"`, { encoding: 'utf-8' });
    console.log(resultBuffer);
    return resultBuffer.trim();
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
    let methodArr: string[] = methodString.split('.');
    methodArr[0] = variableName;
    const replacedString: string = methodArr.join('.');
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

function getCodeOnLine(): [number, string] {
        // Get the active text editor
        const editor = vscode.window.activeTextEditor;
        let lineText = "";
        let lineNumber = 0;
        // Check if there is an active text editor
        if (editor) {
            // Get the position of the cursor (current selection)
            const cursorPosition = editor.selection.active;

            // Get the line number (zero-based) where the cursor is
            lineNumber = cursorPosition.line;

            // Get the text of the line
            lineText = editor.document.lineAt(lineNumber).text;

            // Output the line of code to the console (you can modify this part)
            console.log(`Line ${lineNumber + 1}: ${lineText}`);
        } else {
            vscode.window.showInformationMessage('No active editor.');
        }
        return [lineNumber, lineText];

}

function getCodeOnScreen(): string {
    const editor = vscode.window.activeTextEditor;
    let codeOnScreen = "";
    // Check if there is an active text editor
    if (editor) {
        // Get the visible range of the editor (code on the screen)
        const visibleRange = editor.visibleRanges[0];

        // Get the text within the visible range
        const codeOnScreen = editor.document.getText(visibleRange);

        // Output the code on the screen to the console (you can modify this part)
        console.log('Code on Screen:', codeOnScreen);
    } else {
        vscode.window.showInformationMessage('No active editor.');
    }

    return codeOnScreen;
}

function parseStringToList(input: string): string[] {
    // Remove brackets and single quotes
    const cleanedString = input.replace(/[\[\]']/g, '');

    // Split the string by comma and trim each element
    const stringArray = cleanedString.split(',').map((item) => item.trim());

    return stringArray;
}

function triggerSuggest() {
    vscode.commands.executeCommand('editor.action.triggerSuggest');
}

export function activate(context: vscode.ExtensionContext) {
    // Use the console to output diagnostic information (console.log) and errors (console.error)
	// This line of code will only be executed once when your extension is activated
	console.log('🪩 Codecompletion88 is now active!');
    // const codeOnScreen = getCodeOnScreen();
    // console.log(codeOnScreen);
    // const lineNum = getCodeOnLine()[0];
    // const lineText = getCodeOnLine()[1];
    // console.log(lineNum, lineText);

    initCCSController('FreqCCS');
    // console.log(CCS);

    //TODO: get the local vairaible name
    // const recommendationString = callPythonScript('hello');
    // console.log(recommendationString);
    // const recommendtaions = replaceVariableNameInArray("display", recommendationString);
    // console.log(recommendtaions);
    // dictionary = recommendtaions;


	// The command has been defined in the package.json
	// Now provide the implementation of the command with registerCommand
	// The commandId parameter must match the command field in package.json
	let activator = vscode.commands.registerCommand('codecompletion88.activate', () => {
		vscode.window.showInformationMessage('Codecompletion88 is now active! 🪩');
	});

    let lineSelectionListener = vscode.window.onDidChangeTextEditorSelection((event) => {
        // Check if there is an active text editor
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }

        // Get the selected line numbers
        // const selectedLines = event.selections.map((selection) => selection.active.line);
        // Get the selected lines content
        const visibleRange = editor.visibleRanges[0];

        // Get the text within the visible range
        // const codeOnScreen = editor.document.getText(visibleRange);
        const codeInEditor = editor.document.getText();
        let line = '';
        let lineNumber = -1;

        const fileUri = editor.document.uri;

        // Convert the URI to a file path
        const filePath = fileUri.fsPath;

        // get selected line
        // if (event.selections.length === 1 && event.selections[0].isEmpty) {
        //     // Get the line number where the cursor is
        //     lineNumber = event.selections[0].active.line;

        //     // Get the text of the clicked line
        //     line = editor.document.lineAt(lineNumber).text;

        //     // Output the clicked line to the console (you can modify this part)
        //     console.log('Clicked line:', line);

        //     // return line.text;
        // }

        // get typing line
        if (event.selections.length === 1) {
            const activePosition = event.selections[0].active;
        
            // Get the line number where the cursor is
            lineNumber = activePosition.line;
        
            // Get the text of the line where the cursor is
            line = editor.document.lineAt(lineNumber).text;
        
            // Output the line to the console (you can modify this part)
            console.log('Typed line:', line);
        }


        const CCS_result = callCCSController('FreqCCS', filePath, lineNumber, line.replace(/"/g, '\\"'));
        dictionary = parseStringToList(CCS_result);
        // triggerSuggest();
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

    context.subscriptions.push(activator);
    context.subscriptions.push(lineSelectionListener);
}

// This method is called when your extension is deactivated
export function deactivate() {}