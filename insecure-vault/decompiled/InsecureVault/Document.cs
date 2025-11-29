using System;

namespace InsecureVault;

public class Document
{
	public int Id { get; set; }

	public string Title { get; set; } = "";

	public string DocumentType { get; set; } = "";

	public string FilePath { get; set; } = "";

	public bool IsConfidential { get; set; }

	public DateTime CreatedAt { get; set; }

	public string Content { get; set; } = "REDACTED";
}
