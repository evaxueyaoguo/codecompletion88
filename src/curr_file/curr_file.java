package src.curr_file;

public class curr_file {
  private String text = "init";
  

  public curr_file() {
    int y = 0;
    y++;
  }

  public String toString() {
    int y = 0;
    y ++;
    return text;
  }

  public void setText(String text) {
    //adding a display var here
    String y = 0;
    Display display = new Display();
    //insert here: what method should I call?
    this.text = text;
    System.out.println("text set to: " + y.toString());
  }
  public String getText() {
    return text;
  }
}

// public class HelloWorld {
//   public void anotherMethod() {
// 		// test_text.setLayoutData(null);
// 		Shell shell = new Shell();
// 		shell.setText("Hello World");
// 	}
// }
