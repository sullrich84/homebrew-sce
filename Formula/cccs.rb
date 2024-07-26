class Cccs < Formula
  include Language::Python::Virtualenv

  desc "cccs"
  homepage "https://github.com/sullrich84/homebrew-cccs"
  head "https://github.com/sullrich84/homebrew-cccs.git",
    :branch => "main"

  depends_on "python@3.12"

  resource "argparse" do
    url "https://files.pythonhosted.org/packages/18/dd/e617cfc3f6210ae183374cd9f6a26b20514bbb5a792af97949c5aacddf0f/argparse-1.4.0.tar.gz"
    sha256 "62b089a55be1d8949cd2bc7e0df0bddb9e028faefc8c32038cc84862aefdd6e4"
  end

  def install
    virtualenv_install_with_resources(system_site_packages: false)
  end

  test do
    assert(shell_output("#{bin}/ghq").start_with?("codecentric contacts sync"))
  end

  def post_install
    ohai "✅ Formula has been successfully installed!"
  end
end
