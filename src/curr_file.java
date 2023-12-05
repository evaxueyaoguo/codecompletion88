package src;

public class curr_file {
  private String text = "init";
  int y = 0;

  public curr_file() {
    y++;
  }

  public String toString() {
    y ++;
    return text;
  }

  public void setText(String text) {
    //adding a display var here
    Display display = new Display();
    //insert here: what method should I call?
    this.text = text;
  }
  public String getText() {
    return text;
  }
}
