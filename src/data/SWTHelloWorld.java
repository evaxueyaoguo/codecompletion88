package src.data;
import org.eclipse.swt.SWT;
import org.eclipse.swt.layout.GridData;
import org.eclipse.swt.layout.GridLayout;
import org.eclipse.swt.widgets.Button;
import org.eclipse.swt.widgets.Display;
import org.eclipse.swt.widgets.Label;
import org.eclipse.swt.widgets.Shell;
import org.eclipse.swt.widgets.Text;

// https://github.com/eclipse-platform/eclipse.platform.swt/

// https://github.com/wala/WALA

public class HelloWorld {
	// public Text test_text = new Text();

	public static void main(String[] args) {
		final Display display = new Display();

		final Shell shell = new Shell(display);
// 		StatementExpression(
// 		expression=MethodInvocation(
// 				arguments=[Literal(
// 						postfix_operators=[],
// 						prefix_operators=[],
// 						qualifier=None,
// 						selectors=[],
// 						value="Hello World"*
// 				)],
// 				member=setText,*
// 				postfix_operators=[],
// 				prefix_operators=[],
// 				qualifier=shell,*
// 				selectors=[],
// 				type_arguments=None
// 		),
// 		label=None
// ),
		shell.setText("Hello World"); 
		shell.setLayout(new GridLayout(2, false));

		final Label label = new Label(shell, SWT.LEFT);
		label.setText("Your &Name:");
		label.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, false, false));

		final Text text = new Text(shell, SWT.BORDER | SWT.SINGLE);
		final GridData data = new GridData(SWT.FILL, SWT.CENTER, true, false);
		data.minimumWidth = 120;
		text.setLayoutData(data);

		final Button button = new Button(shell, SWT.PUSH);
		button.setText("Say Hello");
		shell.setDefaultButton(button);
		button.setLayoutData(new GridData(SWT.END, SWT.CENTER, false, false, 2, 1));

		final Label output = new Label(shell, SWT.CENTER);
		output.setLayoutData(new GridData(SWT.FILL, SWT.CENTER, true, false, 2, 1));

		button.addListener(SWT.Selection, event -> {
			String name = text.getText().trim();
			if (name.length() == 0) {
				name = "world";
			}
			output.setText("Hello " + name + "!");
		});

		shell.setSize(shell.computeSize(SWT.DEFAULT, SWT.DEFAULT));
		shell.open();

		while (!shell.isDisposed()) {
			if (!display.readAndDispatch()) {
				display.sleep();
			}
		}

		display.dispose();
	}

	public void anotherMethod() {
		// test_text.setLayoutData(null);
		Shell shell = new Shell();
		shell.setText("Hello World");
	}
}

public class anotherClass{
	public void anotherMethodInAnotherClass() {
		// test_text.setLayoutData(null);
		Shell shell = new Shell();
		shell.setText("Hello World");
	}
}