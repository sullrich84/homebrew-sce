class Sce < Formula
  include Language::Python::Virtualenv

  desc "sce"
  homepage "https://github.com/sullrich84/homebrew-sce"
  head "https://github.com/sullrich84/homebrew-sce.git",
    :branch => "main"

  depends_on "python@3.12"

  resource "argparse" do
    url "https://files.pythonhosted.org/packages/18/dd/e617cfc3f6210ae183374cd9f6a26b20514bbb5a792af97949c5aacddf0f/argparse-1.4.0.tar.gz"
    sha256 "62b089a55be1d8949cd2bc7e0df0bddb9e028faefc8c32038cc84862aefdd6e4"
  end

  resource "slack-sdk" do
    url "https://files.pythonhosted.org/packages/a5/e3/4a2491cbf793bb8da8a51120207df8c097faeda42bf720f7acf7c40e4ca8/slack_sdk-3.31.0.tar.gz"
    sha256 "740d2f9c49cbfcbd46fca56b4be9d527934c225312aac18fd2c0fca0ef6bc935"
  end

  resource "phonenumbers" do
    url "https://files.pythonhosted.org/packages/6f/e0/e75462108e395a8e9dd4f2e97ec72aa11ca4990c962f170d9464197e2fef/phonenumbers-8.13.42.tar.gz"
    sha256 "7137904f2db3b991701e853174ce8e1cb8f540b8bfdf27617540de04c0b7bed5"
  end

  resource "py-phone-number-fmt" do
    url "https://files.pythonhosted.org/packages/d7/1d/2a4274b53675962d19913f9480595eb2c8d60d68d8a9a190116e73f5c14d/py-phone-number-fmt-2.0.0.tar.gz"
    sha256 "9ca9f3d11dc7292d5f156487a734c6265011585354b40de5aae09ca622c390fb"
  end

  def install
    virtualenv_install_with_resources(system_site_packages: false)
  end

  test do
    assert(shell_output("#{bin}/ghq").start_with?("slack contacts exporter"))
  end

  def post_install
    ohai "✅ Formula has been successfully installed!"
  end
end
